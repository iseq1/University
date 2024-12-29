from Hamming_encoding_class import Hamming

if __name__ == '__main__':
    # https://habr.com/ru/articles/140611/
    hamming_obj = Hamming(block_len=8)
    source = input('Укажите слово для работы: ')
    print("||==============||==============||==============||")
    print(f'Длина блока кодирования: {hamming_obj.BLOCK_LENGTH}\n'
          f'Контрольные биты: {hamming_obj.CHECK_BITS}\n'
          f'||==============||==============||==============||')

    encoded_text = hamming_obj.encode(text=source)
    decoded_text = hamming_obj.decode(encoded_text)
    print(f'Закодированное слово: {encoded_text}\n'
          f'Результат декодирования: {decoded_text}\n'
          f'||==============||==============||==============||')

    encoded_with_error = hamming_obj.set_errors(encoded_text)
    diff_index_list = hamming_obj.get_diff_index_list(encoded_text, encoded_with_error)
    decoded_with_error = hamming_obj.decode(encoded_with_error, fix_error=False)
    decoded_and_fix_error = hamming_obj.decode(encoded_with_error, fix_error=True)
    print(f'Закодированное слово c ошибкой: {encoded_with_error}\n'
          f'Допущены ошибки в битах: {diff_index_list}\n'
          f'Результат декодирования без фиксов: {decoded_with_error}\n'
          f'Результат декодирования с фиксами: {decoded_and_fix_error}\n'
          f'||==============||==============||==============||')
