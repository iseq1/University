// 28.02.2022

/*
пробовать ввод-вывод разными средствами
*/

# include <iostream>
# include <cstdlib>
# include <iomanip>
# include <ctime>
# include <fstream>
# include <cstring>

using namespace std;

const int N = 10000;

int a [N], n;

ofstream fout ("array.txt");	// 3904
ofstream bout ("array.bin", ios::binary);	// 4004
ifstream bin ("array-1.bin", ios::binary);	// 4004

/*
0 - описание потока
1 - открытие файла/поток = поток связывается с файлом на диске
2 - анализ открытия = успешно или нет?
3 - ввод-вывод
4 - закрыть файл/поток
*/

int F ();
int FF ();

int main ()
{
	setlocale (LC_ALL, "rus");

	char c, t='@', s [11];
	int n, m, k;

	// заранее создайте файл output.txt!

	fstream f ("output.txt", ios::binary | ios::in | ios::out);
	f.seekg (0, ios::beg);

// в файле все символы пробел заменить на подчеркивание

/*

*/

// демонстрация работы вспомогательных функций

	f.get (c);
//	f.read (s, 1);
//	c = s [0];
	n = f.tellg (), k = f.gcount ();
	m = f.tellp ();
	cout << k << " " << n << " " << m << endl;
	f.read (s, 10);
	n = f.tellg (); k = f.gcount ();
	cout << k << " " << n << " " << m << endl;
	f.seekp (-1, ios::cur);
//	f.write (&t, 1);
	n = f.tellg ();
	cout << n << endl;
	cout << c << endl << s << endl;
	f.put (t);

	// нормальный ввод и копия на экран

	while ( true )
	{
		f.get (c);
		if ( f.eof () )
			break;
		cout << c;
	}

	f.close ();
	return 0;
}

int FF ()	// каждую задачу надо выполнять отдельно, остальные на время закрывать!
{
	// скопировать файл

	char c;
	ifstream bin ("input.txt", ios::binary);
	ofstream bout ("output.txt", ios::binary);

	if ( ! bin.is_open () || ! bout.is_open () )
	{
		cout << "???" << endl;
		return 0;
	}

	while ( true )
	{
		bin.get (c);
		if ( bin.eof () )
			break;
		//
		cout << bin.tellg () << " " << c << " "<< bout.tellp () << endl;
		bout.put (c);
	}

	// узнать и напечатать длину файла
	// прочитать файл до конца
	// узнать текущую позицию

	while ( true )
	{
		bin.get (c);
		if ( bin.eof () )
			break;
	}

	bin.seekg (0, ios::end);	// ios::beg	+	ios::cur
	cout << bin.tellg () << endl;

	// можно ли скопировать файл с помощью такого фрагмента?
	// выводится лишний байт

	while ( ! bin.eof () )
	{
		bin.get (c);
		bout.put (c);
	}

	bin.close();
	bout.close();

	return 0;
}

int F ()	// каждую задачу надо выполнять отдельно, остальные на время закрывать!
{
	// заполняется случайный массив

	for ( int i=0; i < n; i++ )
	{
		a [i] = rand () % 100;
		cout << a [i] << endl;		// '\n'		0X0D0A   CR + LF
	}

	// долгий вывод блоками

	fout << n << endl;
	bout.write ((const char *)& n, sizeof (n));
	for ( int i=0; i < n; i++ )
	{
		fout << a [i] << endl;
		bout.write ((const char *)(a+i), sizeof (int));
	}

	// короткий вывод блоками

	bout.write ((const char *)& n, sizeof (n));
	bout.write ((const char *) a, sizeof (a));


	if ( ! bin.is_open () )
	{
		cout << "???" << endl;
		return 0;
	}

	// читаем размер массива

	bin.read ((char *)& n, sizeof (n));
	cout << n << endl;

	// быстрое чтение массива

	int * b = new int [n];
	bin.read ((char *) b, n*sizeof (int));

	// долгое чтение массива

	for ( int i=0; i < n; i++ )
	{
		bin.read ((char *) & a [i], sizeof (n));
		cout << a [i] << endl;
	}

	fout.close ();
	bin.close ();
	return 0;
}
