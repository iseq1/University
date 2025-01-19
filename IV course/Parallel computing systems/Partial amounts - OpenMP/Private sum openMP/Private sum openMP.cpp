#include <omp.h>
#include <fstream>
#include <cstdlib>
#include <iomanip>
#include <iostream>

const int MAX_ARRAY_LEN = 100000000;
long long array[MAX_ARRAY_LEN];
const int MAX_THREADS = 8;
int thread_counts[MAX_THREADS];
double speedups[MAX_THREADS];

static void fill_array(long long* array, int array_len) {
    for (int i = 0; i < array_len; i++) {
        array[i] = i + 1;  
    }
}

void sequential_sum(long long* arr, int n, int count_block) {
    // Шаг 1: дробление на части
    int block_size = n / count_block; // Размер каждого под-массива
    int remainder = n % count_block;  // Остаток для равномерного распределения

    // Инициализация массива индексов для начала каждого под-массива
    int* starts = (int*)malloc(count_block * sizeof(int));

    int idx = 0;
    for (int i = 0; i < count_block; i++) {
        starts[i] = idx;

        // Для первых 'remainder' блоков, размер будет на 1 больше
        int current_block_size = block_size + (i < remainder ? 1 : 0);
        idx += current_block_size;
    }
   
    // Шаг 2: параллельное вычисление суммы в каждом подмассиве
    for (int i = 0; i < count_block; i++) {
        int start_idx = starts[i];
        int end_idx = (i + 1 < count_block) ? starts[i + 1] : n;

        long long local_sum = 0;
        for (int j = start_idx; j < end_idx; j++) {
            local_sum += arr[j];
        }

        arr[end_idx - 1] = local_sum;
    }

    // Шаг 3: добавляем последний элемент каждого под-массива к следующему
    for (int i = 1; i < count_block; i++) {
        long long add_value = arr[starts[i] - 1]; // Сумма предыдущего подмассива

        for (int j = starts[i]; j < (i + 1 < count_block ? starts[i + 1] : n); j++) {
            arr[j] += add_value;  // Добавляем сумму к каждому элементу следующего подмассива
        }
    }


    // Освобождаем память
    free(starts);
}

void parallel_sum(long long* arr, int n, int num_threads) {
    // Шаг 1: Входящий массив разбиватся на приблизительно равные части относительно количества потоков
    // Шаг 2: В каждом под-массиве параллельно высчитывается сумма - результат записывается в последную ячейку под-массива
    // Шаг 3: После получения сумм каждого под-массива, мы проходимся по каждому под-массиву и складвыаем элементы со значением суммы (последняя ячейка) предыдущего под-массива
    // В итоге в последней ячейке массива юудет результат суммы всего массива
    // 
    // Пример: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]; num_threads = 3;
    // Шаг 1: arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9, 10]] >> под-массивы длиной 3, 3, 4
    // Шаг 2: arr = [[1, 2, 1+2+3], [4, 5, 15], [7, 8, 9, 34]] >> получили суммы под-массивов
    // Шаг 3: arr = [[1, 2, 6], [6+4, 6+5, 6+15], [28, 29, 30, 55]] >> сумма массива = 55


    // Шаг 1: дробление на части
    int block_size = n / num_threads; // Размер каждого под-массива
    int remainder = n % num_threads;  // Остаток для равномерного распределения

    // Инициализация массива индексов для начала каждого под-массива
    int* starts = (int*)malloc(num_threads * sizeof(int));

    int idx = 0; 
    for (int i = 0; i < num_threads; i++) {
        starts[i] = idx;

        // Для первых 'remainder' блоков, размер будет на 1 больше
        int current_block_size = block_size + (i < remainder ? 1 : 0);
        idx += current_block_size;
    }

    // Шаг 2: параллельное вычисление суммы в каждом подмассиве
    #pragma omp parallel num_threads(num_threads)
    {
        int thread_id = omp_get_thread_num();
        int start_idx = starts[thread_id]; 
        int end_idx = (thread_id + 1 < num_threads) ? starts[thread_id + 1] : n;

        long long local_sum = 0;
        for (int i = start_idx; i < end_idx; i++) {
            local_sum += arr[i];
        }

        arr[end_idx - 1] = local_sum;
    }

    // Шаг 3: добавляем последний элемент каждого под-массива к следующему
    for (int i = 1; i < num_threads; i++) {
        long long add_value = arr[starts[i] - 1]; // Сумма предыдущего подмассива
        #pragma omp parallel for
        for (int j = starts[i]; j < (i + 1 < num_threads ? starts[i + 1] : n); j++) {
            arr[j] += add_value;  // Добавляем сумму к каждому элементу следующего подмассива
        }
    }


    // Освобождаем память
    free(starts);
}


int find_optimal_m(int count_block) {
    int optimal_m = -1;

    double seq_begin = -1;
    double seq_duration = -1;

    double paral_begin = -1;
    double paral_duration = -1;

    for (int n = 10; n <= MAX_ARRAY_LEN; n *= 2) {
        fill_array(array, n);

        seq_begin = omp_get_wtime();
        sequential_sum(array, n, count_block);
        seq_duration = omp_get_wtime() - seq_begin;

        paral_begin = omp_get_wtime();
        parallel_sum(array, n, count_block);
        paral_duration = omp_get_wtime() - paral_begin;
        
        std::cout << "Current n = " << n << '\n';
        std::cout << "Posled: " << std::fixed << std::setprecision(10) << seq_duration << "\n";
        std::cout << "Parall: " << std::fixed << std::setprecision(10) << paral_duration << "\n\n";

        if (paral_duration < seq_duration) {
            std::cout << "Optimal M is finded" << "\n";
            optimal_m = n;
            break;
        }
    }

    return optimal_m;
}

void save_optimal_m(int m) {
    std::ofstream out_file("optimal_m.txt");
    if (out_file.is_open()) {
        out_file << m;
        std::cout << "Optimal M = " << m << '\n';
        out_file.close();
        std::cout << "Result have been saved in optimal_m.txt\n\n";
    }
    else {
        std::cerr << "Error while save\n";
    }
}

void get_hybrid_sum(long long* array, int array_len, int M, int count_block) {
    if (array_len >= M) {
        std::cout << "Array length = " << array_len << "; Optimala M = " << M << "; It will be parallel\n";
        parallel_sum(array, array_len, count_block);
    }
    else {
        std::cout << "Array length = " << array_len << "; Optimala M = " << M << "; It will be sequential\n";
        sequential_sum(array, array_len, count_block);
    }
}

int read_optimal_m() {
    int optimal_m = -1;
    std::ifstream in_file("optimal_m.txt");
    if (in_file.is_open()) {
        in_file >> optimal_m;
        in_file.close();
        std::cout << "Optimal M was read from optimal_m.txt\n";
    }
    else {
        std::cerr << "Error while reading\n";
    }
    return optimal_m;
}

void save_speedup_data() {
    std::ofstream out_file("speedup_data.txt");
    if (out_file.is_open()) {
        //out_file << "Number of threads, Speedup" << '\n';
        for (int i = 0; i < MAX_THREADS; ++i) {
            out_file << thread_counts[i] << ',' << speedups[i] << '\n';
        }
        out_file.close();
        std::cout << "Result have been saved in speedup_data.txt\n";
    }
    else {
        std::cerr << "Error while save speedup_data\n";
    }
}


void get_speed_dependence_by_threads(int N, int count_block) {

    double seq_begin = -1;
    double seq_duration = -1;

    double paral_begin = -1;
    double paral_duration = -1;

    fill_array(array, N);
    seq_begin = omp_get_wtime();
    sequential_sum(array, N, count_block);
    seq_duration = omp_get_wtime() - seq_begin;
    std::cout << "Running time of the sequential algorithm " << seq_duration << "\n\n";

    for (int num_threads = 1; num_threads <= MAX_THREADS; ++num_threads) {
        omp_set_num_threads(num_threads);

        fill_array(array, N);
           
        paral_begin = omp_get_wtime();
        parallel_sum(array, N, num_threads);
        paral_duration = omp_get_wtime() - paral_begin;

        double speedup = static_cast<double>(seq_duration) / paral_duration;
        thread_counts[num_threads - 1] = num_threads;
        speedups[num_threads - 1] = speedup;

        std::cout << "Threads " << num_threads << ": \n";
        std::cout << "Running time of the parallel algorithm with " << num_threads << " threads is " << paral_duration << '\n';
        std::cout << "Acceleration with " << num_threads << " threads is " << speedup << "\n\n";
    }
    save_speedup_data();
    int result = system("python plot.py");
}


int main() {
    const int array_len = 1000000;
    fill_array(array, array_len);
    sequential_sum(array, array_len, 8);
        std::cout << "Sun of array: " << array[array_len - 1] << "\n\n";

    fill_array(array, array_len);


    // 1.
    std::cout << "\nTask #1: " << "\n\n";
    parallel_sum(array, array_len, 8);
    std::cout << "Sun of array: " << array[array_len - 1]<<"\n\n";


    // 2.
    fill_array(array, array_len);
    std::cout << "\nTask #2: " << "\n\n";
    save_optimal_m(find_optimal_m(8));

    // 3.
    fill_array(array, array_len);
    std::cout << "\nTask #3: " << "\n\n";
    int M = read_optimal_m();
    if (M == -1) {
        std::cerr << "Error";
        return 1;
    }
    get_hybrid_sum(array, array_len, M, 8);
    std::cout << "Sum of the elements of array: " << array[array_len - 1] << "\n\n";


    // 4.
    fill_array(array, array_len);
    std::cout << "\nTask #4: " << "\n\n";
    get_speed_dependence_by_threads(2*M, 8);

    return 0;
}