#include <omp.h>
#include <fstream>
#include <cstdlib>
#include <iomanip>
#include <iostream>

const int MAX_ARRAY_LEN = 10000000;
int array[MAX_ARRAY_LEN];
const int MAX_THREADS = 8;
int thread_counts[MAX_THREADS];
double speedups[MAX_THREADS];

static void fill_array(int* array, int array_len) {
    for (int i = 0; i < array_len; i++) {
        array[i] = i + 1;  
    }
}

void sequential_sum(int* array, int array_len) {
    for (int i = 1; i < array_len; ++i) {
        array[i] += array[i - 1];
    }
}

void parallel_sum(int* array, int array_len) {
    #pragma omp parallel for schedule(guided)
    for (int i = 1; i < array_len; ++i) {
        #pragma omp atomic
        array[i] += array[i - 1];  // Частичная сумма для текущего элемента
    }
}

int find_optimal_m() {
    int optimal_m = -1;

    double seq_begin = -1;
    double seq_duration = -1;

    double paral_begin = -1;
    double paral_duration = -1;

    for (int n = 10; n <= MAX_ARRAY_LEN; n *= 2) {
        fill_array(array, n);

        seq_begin = omp_get_wtime();
        sequential_sum(array, n);
        seq_duration = omp_get_wtime() - seq_begin;

        paral_begin = omp_get_wtime();
        parallel_sum(array, n);
        paral_duration = omp_get_wtime() - paral_begin;
        
        std::cout << n << '\n';
        std::cout << "Posled: " << std::fixed << std::setprecision(10) << seq_duration << "\n";
        std::cout << "Parall: " << std::fixed << std::setprecision(10) << paral_duration << "\n\n";

        if (paral_duration < seq_duration) {
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
        std::cout << "Result have been saved in optimal_m.txt\n";
    }
    else {
        std::cerr << "Error while save\n";
    }
}

void get_hybrid_sum(int* array, int array_len, int M) {
    if (array_len >= M) {
        std::cout << "Array length = " << array_len << "; Optimala M = " << M << "; It will be parallel\n";
        parallel_sum(array, array_len);
    }
    else {
        std::cout << "Array length = " << array_len << "; Optimala M = " << M << "; It will be sequential\n";
        sequential_sum(array, array_len);
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


void get_speed_dependence_by_threads(int N) {

    double seq_begin = -1;
    double seq_duration = -1;

    double paral_begin = -1;
    double paral_duration = -1;

    fill_array(array, N);
    seq_begin = omp_get_wtime();
    sequential_sum(array, N);
    seq_duration = omp_get_wtime() - seq_begin;
    std::cout << "Running time of the sequential algorithm " << seq_duration << '\n';

    for (int num_threads = 1; num_threads <= MAX_THREADS; ++num_threads) {
        omp_set_num_threads(num_threads);

        fill_array(array, N);
           
        paral_begin = omp_get_wtime();
        parallel_sum(array, N);
        paral_duration = omp_get_wtime() - paral_begin;

        double speedup = static_cast<double>(seq_duration) / paral_duration;
        thread_counts[num_threads - 1] = num_threads;
        speedups[num_threads - 1] = speedup;

        std::cout << "Running time of the parallel algorithm with " << num_threads << "threads is " << paral_duration << '\n';
        std::cout << "Acceleration with " << num_threads << " threads is " << speedup << '\n';
    }
    save_speedup_data();
    int result = system("python plot.py");
}


int main() {
    const int array_len = 100000;
    fill_array(array, array_len);

    // 1.
    parallel_sum(array, array_len);
    //std::cout << array[array_len - 1]<<'\n';


    // 2.
    save_optimal_m(find_optimal_m());

    // 3.
    int M = read_optimal_m();
    if (M == -1) {
        std::cerr << "Error";
        return 1;
    }
    get_hybrid_sum(array, array_len, M);

    // 4.
    get_speed_dependence_by_threads(2*M);

    return 0;
}