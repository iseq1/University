#include <iostream>
#include <omp.h>
#include <vector>
#include <forward_list>
using namespace std;
const int arr_len = 100000;
int digitals[arr_len] = { };
const int N = 10000, M = 10000;
int A[N][M];



static void Shuffle_array() {
    for (int i = arr_len; i > 0; i--) {
        digitals[i] = i;
    }
}

static void Bubble_Parallel() {
    double begin = omp_get_wtime();
    for (int i = 0; i < arr_len; i++) {
#pragma omp  for schedule(guided, 4)
            for (int j = i%2; j < arr_len - 1; j += 2) {
                if (digitals[j] > digitals[j + 1]) {
                    int b = digitals[j];
                    digitals[j] = digitals[j + 1];
                    digitals[j + 1] = b;
                }
            }
    }
    double duration = omp_get_wtime() - begin;
    cout <<"Parallel " << duration << endl;
   
    return;
}

static void Bubble() {
    
    double begin = omp_get_wtime();

    for (int i = 0; i < arr_len; i++) {
        for (int j = 0; j < arr_len-1; j++) {
            if (digitals[j] > digitals[j + 1]) {
                int b = digitals[j]; 
                digitals[j] = digitals[j + 1];
                digitals[j + 1] = b; 
            }
        }
    }
    double duration = omp_get_wtime() - begin;
    cout << "No parallel " << duration << endl;
    return;
}

static void Bubble_Parallel_By_Schedule(char name, int chunks) {
    double begin = -1;
    double duration = -1;
    switch (name) {
        case 's':
            begin = omp_get_wtime();
            for (int i = 0; i < arr_len; i++) {
                #pragma omp  for schedule(static, chunks)
                for (int j = i % 2; j < arr_len - 1; j += 2) {
                    if (digitals[j] > digitals[j + 1]) {
                        int b = digitals[j];
                        digitals[j] = digitals[j + 1];
                        digitals[j + 1] = b;
                    }
                }
            }
            duration = omp_get_wtime() - begin;
            cout << "Parallel_schedule_static_by_" << chunks << ": " << duration << endl;
            break;
        case 'd':
            begin = omp_get_wtime();
            for (int i = 0; i < arr_len; i++) {
                #pragma omp  for schedule(dynamic, chunks)
                for (int j = i % 2; j < arr_len - 1; j += 2) {
                    if (digitals[j] > digitals[j + 1]) {
                        int b = digitals[j];
                        digitals[j] = digitals[j + 1];
                        digitals[j + 1] = b;
                    }
                }
            }
            duration = omp_get_wtime() - begin;
            cout << "Parallel_schedule_dynamic_by_" << chunks << ": " << duration << endl;
            break;
        case 'g':
            begin = omp_get_wtime();
            for (int i = 0; i < arr_len; i++) {
#               pragma omp  for schedule(guided, chunks)
                for (int j = i % 2; j < arr_len - 1; j += 2) {
                    if (digitals[j] > digitals[j + 1]) {
                        int b = digitals[j];
                        digitals[j] = digitals[j + 1];
                        digitals[j + 1] = b;
                    }
                }
            }
            duration = omp_get_wtime() - begin;
            cout << "Parallel_schedule_guided_by_" << chunks << ": " << duration << endl;
            break;
        default:
            

            std::cout << "Name is uncorrect.\n It is would be: ['s', 'd', 'g']" << "\n";
            break;
    }
    
    return;
}

static int Sum_of_elements_array(char name) {
    double begin = -1;
    double duration = -1;
    int sum = 0;
    int local_sum = 0; // Локальная сумма для каждого потока
    switch (name) {
        case 's':
            // Последовательно
            begin = omp_get_wtime();
            for (int i = 0; i < arr_len; i++)
                sum = sum + digitals[i];
            duration = omp_get_wtime() - begin;
            cout << "Posledovatel`no: " << duration << endl;
            break;
        case 'p':
            // Параллельно
            begin = omp_get_wtime();
            #pragma omp parallel for
            for (int i = 0; i < arr_len; i++)
                sum = sum + digitals[i];
            duration = omp_get_wtime() - begin;
            cout << "Parallel: " << duration << endl;
            break;
        case 'r':
            // reduction
            begin = omp_get_wtime();
            #pragma omp parallel for reduction(+:local_sum)
            for (int i = 0; i < arr_len; i++) {
                local_sum += digitals[i]; // Каждое обновление происходит локально
            }
            sum = local_sum; 
            duration = omp_get_wtime() - begin;
            cout << "Reduction: " << duration << endl;
            break;
        case 'a':
            // atomic
            begin = omp_get_wtime();
            #pragma omp parallel for
            for (int i = 0; i < arr_len; i++) {
                #pragma omp atomic
                sum += digitals[i]; // Атомарное обновление суммы
            }
            duration = omp_get_wtime() - begin;
            cout << "Atomic: " << duration << endl;
            break;
        case 'c':
            // critical
            begin = omp_get_wtime();
            //#pragma omp parallel for
            //for (int i = 0; i < arr_len; i++) {
            //    #pragma omp critical
            //    sum += digitals[i]; // Обновление суммы в критической секции
            //}

            #pragma omp parallel sections
            {
                #pragma omp section
                for (int i = 0; i < arr_len; i++) {
                    #pragma omp critical(sum)
                    sum += digitals[i]; // Обновление суммы в критической секции
                }
            }

            duration = omp_get_wtime() - begin;
            cout << "Critical: " << duration << endl;
            break;
        case 'm':
            // Мьютекс
            omp_lock_t lock;
            omp_init_lock(&lock);
            begin = omp_get_wtime();
            #pragma omp parallel for shared(lock)
            for (int i = 0; i < arr_len; i++) {
                omp_set_lock(&lock);
                sum += digitals[i]; 
                omp_unset_lock(&lock);
            }
            duration = omp_get_wtime() - begin;
            omp_destroy_lock(&lock);
            cout << "Mutex: " << duration << endl;

            break;
    }
    return sum;
}

static int Shift_of_elems(char name) {
    double begin = -1;
    double duration = -1;
    int max_threads = omp_get_max_threads();
    // Используем вектор для хранения первых элементов каждой секции
    std::vector<int> first_elements(max_threads);

    switch (name) {
        case 's':
            // Последовательно
            begin = omp_get_wtime();
            for (int i = 0; i < arr_len; i++)
                if (i == arr_len - 1) {
                    digitals[0] = digitals[i];
                }
                else {
                    digitals[i] = digitals[i + 1];
                }
            duration = omp_get_wtime() - begin;
            cout << "Posledovatel`no: " << duration << endl;
            break;
        case 'p':
            // Параллельно
            

            break;
    }
    return digitals[0];
}

struct Node {
    int value;
    Node* next;

    Node(int _val) : value(_val), next(nullptr) {}
};

struct list {
    Node* first;
    Node* last;

    list() : first(nullptr), last(nullptr) {}

    bool is_empty() {
        return first == nullptr;
    }

    void push_end(int _val) {
        Node* p = new Node(_val);
        if (is_empty()) {
            first = p;
            last = p;
            return;
        }
        last->next = p;
        last = p;
    }

    void push_front(int _val) {
        Node* p = new Node(_val);
        p->next = first;
        first = p;
    }

    void print() {
        if (is_empty()) return;
        Node* p = first;
        while (p) {
            cout << p->value << " ";
            p = p->next;
        }
        cout << endl;
    }

    Node* operator[] (const int index) {
        if (is_empty()) return nullptr;
        Node* p = first;
        for (int i = 0; i < index; i++) {
            p = p->next;
            if (!p) return nullptr;
        }
        return p;
    }
};

static void Array_n_List_battle() {
    double begin_arr = -1;
    double duration_arr = -1;
    int sum_arr = 0;

    double begin_lst = -1;
    double duration_lst = -1;
    int sum_lst = 0;

    Shuffle_array();
    list lst;
    for (int i = 0; i < arr_len; i++) {
        lst.push_front(i);
    }

    begin_arr = omp_get_wtime();
    for (int i = 0; i < arr_len; i++) {
        sum_arr += digitals[i]; 
    }
    duration_arr = omp_get_wtime() - begin_arr;
    cout << "TIme of Sum(array): " << duration_arr << " || sum = " << sum_arr << endl;


    begin_lst = omp_get_wtime();
   
    Node* p = lst[0];
    while (p) {
        sum_lst += p->value;
        p = p->next;
    }
    
        
    duration_lst = omp_get_wtime() - begin_lst;
    cout << "TIme of Sum(list): " << duration_lst << " || sum = " << sum_lst << endl;
}

static void multiply_matrix(char name) {

    double begin = -1;
    double duration = -1;

    const int N = 10, M = 10;
    int A[N][M], B[N][M], C[N][M];
    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++)
            A[i][j] = i+j, B[i][j] = i+j;
    switch (name) {
        case 's':
            begin = omp_get_wtime();
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < M; j++) {
                    for (int k = 0; k < N; k++) {
                        int save = A[i][k] * B[k][j];
                        C[i][j] += save;
                        save = 0;
                    }
                }
            }
            duration = omp_get_wtime() - begin;
            cout << "Posledovatel`no: " << duration << endl;

    }


}

static void matrix_step(char name) {
    double begin = -1;
    double duration = -1;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++)
            A[i][j] = i + j;
    long long sum = 0;

    switch (name) {
        case 'r':
            begin = omp_get_wtime();
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < M; j++) {
                    sum += A[i][j];
                }
            }
            duration = omp_get_wtime() - begin;
            cout << "Step by rows: " << duration << endl;
            cout << "Sum: " << sum << endl;
            break;
        case 'c':
            begin = omp_get_wtime();
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < M; j++) {
                    sum += A[j][i];
                }
            }
            duration = omp_get_wtime() - begin;
            cout << "Step by coloms: " << duration << endl;
            cout << "Sum: " << sum << endl;
            break;
        default:
            cout << "Incorrect input";
            break;
    }

}

// < сумма элементов масива последовательно/параллельно/reduction/atomic/critical/mutex >
// параллельный сдвиг элементов массива на 1 позицию влево 
// < Сравнить время суммирования элементов массива и односвязного списка (что и во сколько быстрее?) >
// Перемножить две матрицы последовательно и параллельно(разными способами) + мб надо будет время засекать 
// Обойти матрицу по строкам и по столбцам и замерить что быстрее
int main()
{
    //Shuffle_array();
    matrix_step('r');
    matrix_step('c');


    //Array_n_List_battle();
    
    //multiply_matrix('s');


    //Shuffle_array();
    //cout << "First elem before activities : " << digitals[0] << endl << endl;
    //cout << "First elem: " << Shift_of_elems('s') << endl << endl;

    //Shuffle_array();
    //for (int i = arr_len_min; i > 0; i--) {
    //    digitals_min[i] = i;
    //}
    //cout << "First elem: " << Shift_of_elems('p') << endl << endl;
    

    
    
    //Shuffle_array();
    //cout<<"Sum of array: "<<Sum_of_elements_array('s')<<endl<<endl;
    //cout<<"Sum of array: "<<Sum_of_elements_array('p')<< " There are data race" << endl << endl;
    //cout << "Sum of array: " << Sum_of_elements_array('r') << endl << endl;
    //cout << "Sum of array: " << Sum_of_elements_array('a') << endl << endl;
    //cout << "Sum of array: " << Sum_of_elements_array('c') << endl << endl;
    //cout << "Sum of array: " << Sum_of_elements_array('m') << endl << endl;


   //Bubble();
   //Bubble_Parallel();

    //Shuffle_array();
    //Bubble();
    
    //Shuffle_array();
    //Bubble_Parallel_By_Schedule('s', 1);
    
    //Shuffle_array();
    //Bubble_Parallel_By_Schedule('s', 4);
    
    //Shuffle_array();
    //Bubble_Parallel_By_Schedule('s', 8);
    
    //Shuffle_array();
    //Bubble_Parallel_By_Schedule('d', 1);
    
    //Shuffle_array();
    //Bubble_Parallel_By_Schedule('d', 4);
    
    //Shuffle_array();
    //Bubble_Parallel_By_Schedule('d', 8);
    
    //Shuffle_array();
    //Bubble_Parallel_By_Schedule('g', 1);
    
    //Shuffle_array();
    //Bubble_Parallel_By_Schedule('g', 4);
    
    //Shuffle_array();
    //Bubble_Parallel_By_Schedule('g', 8);
    
    //Bubble_Parallel_By_Schedule('u', 8);

    return 0;
}
