import copy
import time

import numpy as np

m = 4
k_ols = m * m
k_sec_ded = 16
n = 48


def get_check_bits(data_bits, data_e_bits):
    co_out = np.zeros(k_ols, dtype=int)

    co_out[0] = data_bits[0] ^ data_bits[1] ^ data_bits[2] ^ data_bits[3]
    co_out[1] = data_bits[4] ^ data_bits[5] ^ data_bits[6] ^ data_bits[7]
    co_out[2] = data_bits[8] ^ data_bits[9] ^ data_bits[10] ^ data_bits[11]
    co_out[3] = data_bits[12] ^ data_bits[13] ^ data_bits[14] ^ data_bits[15]

    co_out[4] = data_bits[0] ^ data_bits[4] ^ data_bits[8] ^ data_bits[12]
    co_out[5] = data_bits[1] ^ data_bits[5] ^ data_bits[9] ^ data_bits[13]
    co_out[6] = data_bits[2] ^ data_bits[6] ^ data_bits[10] ^ data_bits[14]
    co_out[7] = data_bits[3] ^ data_bits[7] ^ data_bits[11] ^ data_bits[15]

    co_out[8] = data_bits[0] ^ data_bits[5] ^ data_bits[10] ^ data_bits[15]
    co_out[9] = data_bits[1] ^ data_bits[4] ^ data_bits[11] ^ data_bits[14]
    co_out[10] = data_bits[2] ^ data_bits[7] ^ data_bits[8] ^ data_bits[13]
    co_out[11] = data_bits[3] ^ data_bits[6] ^ data_bits[9] ^ data_bits[12]

    co_out[12] = data_bits[0] ^ data_bits[6] ^ data_bits[11] ^ data_bits[13]
    co_out[13] = data_bits[1] ^ data_bits[7] ^ data_bits[10] ^ data_bits[12]
    co_out[14] = data_bits[2] ^ data_bits[4] ^ data_bits[9] ^ data_bits[15]
    co_out[15] = data_bits[3] ^ data_bits[5] ^ data_bits[8] ^ data_bits[14]

    ce_out = np.zeros(k_sec_ded, dtype=int)

    ce_out[0] = data_e_bits[0] ^ data_e_bits[1] ^ data_e_bits[2]
    ce_out[1] = data_e_bits[0] ^ data_e_bits[1] ^ data_e_bits[3]
    ce_out[2] = data_e_bits[0] ^ data_e_bits[2] ^ data_e_bits[3]
    ce_out[3] = data_e_bits[1] ^ data_e_bits[2] ^ data_e_bits[3]

    ce_out[4] = data_e_bits[4] ^ data_e_bits[5] ^ data_e_bits[6]
    ce_out[5] = data_e_bits[4] ^ data_e_bits[5] ^ data_e_bits[7]
    ce_out[6] = data_e_bits[4] ^ data_e_bits[6] ^ data_e_bits[7]
    ce_out[7] = data_e_bits[5] ^ data_e_bits[6] ^ data_e_bits[7]

    ce_out[8] = data_e_bits[8] ^ data_e_bits[9] ^ data_e_bits[10]
    ce_out[9] = data_e_bits[8] ^ data_e_bits[9] ^ data_e_bits[11]
    ce_out[10] = data_e_bits[8] ^ data_e_bits[10] ^ data_e_bits[11]
    ce_out[11] = data_e_bits[9] ^ data_e_bits[10] ^ data_e_bits[11]

    ce_out[12] = data_e_bits[12] ^ data_e_bits[13] ^ data_e_bits[14]
    ce_out[13] = data_e_bits[12] ^ data_e_bits[13] ^ data_e_bits[15]
    ce_out[14] = data_e_bits[12] ^ data_e_bits[14] ^ data_e_bits[15]
    ce_out[15] = data_e_bits[13] ^ data_e_bits[14] ^ data_e_bits[15]

    c_out = np.zeros(k_ols, dtype=int)
    for i in range(k_ols):
        c_out[i] = co_out[i] ^ ce_out[i]

    return c_out


def correct_error(data_flip, data_e_flip, c_out, c_out_flip):
    s_out = np.zeros(k_ols, dtype=int)
    for i in range(16):
        s_out[i] = c_out[i] ^ c_out_flip[i]

    # ols
    d_ols_c = np.zeros(k_ols, dtype=int)

    # 1st 4 bits
    d1_s = np.array([s_out[0], s_out[4], s_out[8], s_out[12]])
    majority = np.argmax(np.bincount(d1_s))
    d_ols_c[0] = majority ^ data_flip[0]

    d2_s = np.array([s_out[0], s_out[5], s_out[9], s_out[13]])
    majority = np.argmax(np.bincount(d2_s))
    d_ols_c[1] = majority ^ data_flip[1]

    d3_s = np.array([s_out[0], s_out[6], s_out[10], s_out[14]])
    majority = np.argmax(np.bincount(d3_s))
    d_ols_c[2] = majority ^ data_flip[2]

    d4_s = np.array([s_out[0], s_out[7], s_out[11], s_out[15]])
    majority = np.argmax(np.bincount(d4_s))
    d_ols_c[3] = majority ^ data_flip[3]

    # 2nd 4 bits
    d5_s = np.array([s_out[1], s_out[4], s_out[9], s_out[14]])
    majority = np.argmax(np.bincount(d5_s))
    d_ols_c[4] = majority ^ data_flip[4]

    d6_s = np.array([s_out[1], s_out[5], s_out[8], s_out[15]])
    majority = np.argmax(np.bincount(d6_s))
    d_ols_c[5] = majority ^ data_flip[5]

    d7_s = np.array([s_out[1], s_out[6], s_out[11], s_out[12]])
    majority = np.argmax(np.bincount(d7_s))
    d_ols_c[6] = majority ^ data_flip[6]

    d8_s = np.array([s_out[1], s_out[5], s_out[10], s_out[13]])
    majority = np.argmax(np.bincount(d8_s))
    d_ols_c[7] = majority ^ data_flip[7]

    # 3rd 4 bits
    d9_s = np.array([s_out[2], s_out[4], s_out[10], s_out[15]])
    majority = np.argmax(np.bincount(d9_s))
    d_ols_c[8] = majority ^ data_flip[8]

    d10_s = np.array([s_out[2], s_out[5], s_out[11], s_out[14]])
    majority = np.argmax(np.bincount(d10_s))
    d_ols_c[9] = majority ^ data_flip[9]

    d11_s = np.array([s_out[2], s_out[6], s_out[8], s_out[13]])
    majority = np.argmax(np.bincount(d11_s))
    d_ols_c[10] = majority ^ data_flip[10]

    d12_s = np.array([s_out[2], s_out[7], s_out[9], s_out[12]])
    majority = np.argmax(np.bincount(d12_s))
    d_ols_c[11] = majority ^ data_flip[11]

    # last 4 bits
    d13_s = np.array([s_out[3], s_out[4], s_out[11], s_out[13]])
    majority = np.argmax(np.bincount(d13_s))
    d_ols_c[12] = majority ^ data_flip[12]

    d14_s = np.array([s_out[3], s_out[5], s_out[10], s_out[12]])
    majority = np.argmax(np.bincount(d14_s))
    d_ols_c[13] = majority ^ data_flip[13]

    d15_s = np.array([s_out[3], s_out[6], s_out[9], s_out[15]])
    majority = np.argmax(np.bincount(d15_s))
    d_ols_c[14] = majority ^ data_flip[14]

    d16_s = np.array([s_out[3], s_out[7], s_out[14], s_out[15]])
    majority = np.argmax(np.bincount(d16_s))
    d_ols_c[15] = majority ^ data_flip[15]

    ################################################

    # sec-ded
    de_sec_ded_c = np.zeros(k_ols, dtype=int)

    # 1st 4 bits
    de1_s = s_out[0] and s_out[1] and s_out[2] and not s_out[3]
    de_sec_ded_c[0] = de1_s ^ data_e_flip[0]

    de2_s = s_out[0] and s_out[1] and s_out[3] and not s_out[2]
    de_sec_ded_c[1] = de2_s ^ data_e_flip[1]

    de3_s = s_out[0] and s_out[2] and s_out[3] and not s_out[1]
    de_sec_ded_c[2] = de3_s ^ data_e_flip[2]

    de4_s = s_out[1] and s_out[2] and s_out[3] and not s_out[0]
    de_sec_ded_c[3] = de4_s ^ data_e_flip[3]

    # 2nd 4 bits
    de5_s = s_out[4] and s_out[5] and s_out[6] and not s_out[7]
    de_sec_ded_c[4] = de5_s ^ data_e_flip[4]

    de6_s = s_out[4] and s_out[5] and s_out[7] and not s_out[6]
    de_sec_ded_c[5] = de6_s ^ data_e_flip[5]

    de7_s = s_out[4] and s_out[6] and s_out[7] and not s_out[5]
    de_sec_ded_c[6] = de7_s ^ data_e_flip[6]

    de8_s = s_out[5] and s_out[6] and s_out[7] and not s_out[4]
    de_sec_ded_c[7] = de8_s ^ data_e_flip[7]

    # 3rd 4 bits
    de9_s = s_out[8] and s_out[9] and s_out[10] and not s_out[11]
    de_sec_ded_c[8] = de9_s ^ data_e_flip[8]

    de10_s = s_out[8] and s_out[9] and s_out[11] and not s_out[10]
    de_sec_ded_c[9] = de10_s ^ data_e_flip[9]

    de11_s = s_out[8] and s_out[10] and s_out[11] and not s_out[9]
    de_sec_ded_c[10] = de11_s ^ data_e_flip[10]

    de12_s = s_out[9] and s_out[10] and s_out[11] and not s_out[8]
    de_sec_ded_c[11] = de12_s ^ data_e_flip[11]

    # Last 4 bits
    de13_s = s_out[12] and s_out[13] and s_out[14] and not s_out[15]
    de_sec_ded_c[12] = de13_s ^ data_e_flip[12]

    de14_s = s_out[12] and s_out[13] and s_out[15] and not s_out[14]
    de_sec_ded_c[13] = de14_s ^ data_e_flip[13]

    de15_s = s_out[12] and s_out[14] and s_out[15] and not s_out[13]
    de_sec_ded_c[14] = de15_s ^ data_e_flip[14]

    de16_s = s_out[13] and s_out[14] and s_out[15] and not s_out[12]
    de_sec_ded_c[15] = de16_s ^ data_e_flip[15]

    return d_ols_c, de_sec_ded_c


def get_single_error_correct_stats(data_word, c_out):
    error_corrected = 0
    correct_failed = 0
    decode_time = 0
    for i in range(0, 32):
        data_word_flip = copy.deepcopy(data_word)
        data_word_flip[i] = not data_word[i]

        data_flip = data_word_flip[0:16]
        data_e_flip = data_word_flip[16:32]

        start_time = time.time()
        c_out_flip = get_check_bits(data_flip, data_e_flip)
        d_ols_c, de_sec_ded_c = correct_error(data_flip, data_e_flip, c_out, c_out_flip)
        data_word_corrected = np.concatenate((d_ols_c, de_sec_ded_c), axis=0)
        end_time = time.time()
        decode_time += end_time - start_time

        if np.array_equal(data_word, data_word_corrected):
            error_corrected += 1
        else:
            correct_failed += 1
            # print("d_ols_i:", data_orig, "\nd_ols_f:", data_flip, "\nd_ols_c:", d_ols_c)
            # print("de_sec_ded_i:", data_e_orig, "\nde_sec_ded_f:", data_e_flip, "\nde_sec_ded_c:", de_sec_ded_c)

    percentage = 100 * error_corrected / (error_corrected + correct_failed)
    avg_execution_time = 1000 * (encode_time + decode_time / (error_corrected + correct_failed))
    print("Single Error Corrected: {0}, Failed: {1}, Percentage Corrected: {2}, Average Time: {3} ms".format(
        error_corrected, correct_failed, percentage, avg_execution_time
    ))

def get_double_error_correct_stats(data_word, c_out):
    error_corrected = 0
    correct_failed = 0
    decode_time = 0
    for i in range(32):
        for j in range(32):
            data_word_flip = copy.deepcopy(data_word)
            if (i + j) < 32:
                data_word_flip[i] = not data_word[j]
                data_word_flip[i + j] = not data_word[i + j]
            else:
                break

            data_flip = data_word_flip[0:16]
            data_e_flip = data_word_flip[16:32]

            start_time = time.time()
            c_out_flip = get_check_bits(data_flip, data_e_flip)
            d_ols_c, de_sec_ded_c = correct_error(data_flip, data_e_flip, c_out, c_out_flip)
            data_word_corrected = np.concatenate((d_ols_c, de_sec_ded_c), axis=0)
            end_time = time.time()
            decode_time += end_time - start_time

            if np.array_equal(data_word, data_word_corrected):
                error_corrected += 1
            else:
                correct_failed += 1
                # print("d_ols_i:", data_orig, "\nd_ols_f:", data_flip, "\nd_ols_c:", d_ols_c)
                # print("de_sec_ded_i:", data_e_orig, "\nde_sec_ded_f:", data_e_flip, "\nde_sec_ded_c:", de_sec_ded_c)

    percentage = 100 * error_corrected / (error_corrected + correct_failed)
    avg_execution_time = 1000 * (encode_time + decode_time / (error_corrected + correct_failed))
    print("Double Error Corrected: {0}, Failed: {1}, Percentage Corrected: {2}, Average Time: {3} ms".format(
        error_corrected, correct_failed, percentage, avg_execution_time
    ))


if __name__ == "__main__":
    # Encoder
    print("DataWord Size: 32bit")
    start_time = time.time()
    data_word = np.array(list('10101010010101011010100101010101'), dtype=int)
    data_orig = data_word[0:16]
    data_e_orig = data_word[16:32]
    c_out = get_check_bits(data_orig, data_e_orig)
    end_time = time.time()
    encode_time = end_time - start_time

    # Single Error Inject and Decode
    get_single_error_correct_stats(data_word, c_out)

    # Double Error Inject and Decode
    get_double_error_correct_stats(data_word, c_out)
