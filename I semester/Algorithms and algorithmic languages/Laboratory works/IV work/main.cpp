/*
4. В прямоугольной матрице целых чисел размера n на m найти прямоугольник
самой большой площади, состоящий только из единиц, и напечатать эту площадь
(площадь = количество строк х количество столбцов). В первой строке задаются числа n и m,
а в последующих – сама матрица.
Исходные данные:
3 4
1 0 1 1
0 0 1 1
1 0 0 0
Результат:
4
1.6.3.6. Прямоугольник с наибольшей суммой. В прямоугольной матрице целых чисел
размера n на m найти прямоугольник с наибольшей суммой и напечатать эту сумму.
В первой строке задаются числа n и m, а в последующих – сама матрица.
Исходные данные:
3 4
1 -2 3 2
2 3 -4 1
3 -5 3 0
Результат:
6
*/

#include <iostream>
using namespace std;
int MaxAreaMatrix(int **a, int n, int m);
int MaxAreaRectangle(int **a, int n, int m, int i, int j);
int MaxSumMatrix(int **a, int n, int m);
int MaxSumRectangle(int **a, int bottom, int right, int **val);
int main() {
    int n, m; cin >> n >> m;
    int **a = new int*[n];
    for(int i = 0; i < n; i++){
        a[i] = new int[m];
        for(int j = 0; j < m; j++){
            cin >> a[i][j];
        }
    }

    cout << MaxSumMatrix(a, n, m);
}
//Площадь
int MaxAreaMatrix(int **a, int n, int m){
    int maxArea = 0;
    for(int i = 0; i < n; i++){
        for(int j = 0; j < m; j++){
            if(a[i][j] != 0){
                maxArea = max(maxArea, MaxAreaRectangle(a, n, m, i, j));
            }
        }
    }
    return maxArea;
}
int MaxAreaRectangle(int **a, int n, int m, int row, int col){
    int maxArea = 0;
    int right = m-1;
    int bot = n-1;
    for(int i = row; i <= bot; i++){
        for(int j = col; j <= right; j++){
            if(a[i][j] == 0 || j == right && a[i][j] == 1){
                int s;
                if(a[i][j] == 0){
                    s = (j - col)*(i - row + 1);
                    right = j-1;
                }
                else{
                    s = (j - col + 1)*(i - row + 1);
                }
                maxArea = max(maxArea, s);
            }
            if(a[i][col] == 0){
                bot = i-1;
            }
        }
    }
    return maxArea;
}
//Сумма
int MaxSumMatrix(int **a, int n, int m){
    int maxSum = INT_MIN;
    int **val = new int*[n];
    for(int i = 0; i < n; i++){
        val[i] = new int[m];
        for(int j = 0; j < m; j++){
            val[i][j] = a[i][j];
            if(i != 0){
                val[i][j] += val[i-1][j];
            }
            if(j != 0){
                val[i][j] += val[i][j-1];
            }
            if(i != 0 && j != 0){
                val[i][j] -= val[i-1][j-1];
            }

            maxSum = max(maxSum, MaxSumRectangle(a, i, j, val));
        }
    }
    return maxSum;
}
int MaxSumRectangle(int **a, int bottom, int right, int **val){
    int maxSum = INT_MIN;
    int sum = val[bottom][right];
    for(int i = 0; i <= bottom; i++){
        for(int j = 0; j <= right; j++){
            if(i != 0){
                sum -= val[i-1][right];
            }
            if(j != 0){
                sum -= val[bottom][j-1];
            }
            if(i != 0 && j != 0){
                sum += val[i-1][j-1];
            }
            maxSum = max(maxSum, sum);
        }
    }
    return maxSum;
}