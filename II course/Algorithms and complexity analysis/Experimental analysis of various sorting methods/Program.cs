using System;
using System.Collections.Generic;
using System.Data;
using System.Diagnostics;
using System.Linq;
using System.IO;
using Microsoft.Office.Interop.Excel;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;

namespace Experimental_analysis_of_various_sorting_methods
{
    internal class Program
    {
        /*
        
        1. Реализовать различные методы сортировки и проверить на практике оценки их сложности:
            · простые схемы (сортировка вставками, пузырьковая, выбором и т.д.) + + + + +
            · сортировка Шелла (с различными длинами промежутков)   +
            · быстрая сортировка    +
            · сортировка слиянием   +
            · сортировка кучей      +
            · поразрядная сортировка    +
            · встроенная в язык программирования сортировка +
        2. Сравнить их между собой на различных входных данных:
            · массивах различных типов
                - массивах цифр (от 0 до 9) (однобайтовый тип данных)   +
                - массивах чисел     + 
                - массивах строк     +
                - массивах структур (например, дат)
            · массивах различной длины (малой – до 100, средней – до 10000, большой – до 1000000 элементов), например:
                - порядка 50 элементов          +
                - порядка 500 элементов         +
                - порядка 5000 элементов        +  
                - порядка 50000 элементов       +
                - порядка 500000 элементов      +
                - другие варианты? Плавное увеличение размера с некоторым шагом?
            · по-разному порожденных массивах, например:
                - случайно сгенерированных - СГ
                - частично упорядоченных (вставка нескольких элементов в упорядоченный, частичное перемешивание, «неупорядоченный хвост» и т.п.) - ЧУ
                - большая доля одинаковых элементов - БДОУ
            
        */
        
        //Была попытка не генерировать строки заданной длины, а брать слова из словаря через api, но это медленее и нет гарантии, что в словаре есть n слов заданной длины, где n может быть n=500000

        struct DateRange
        {
            public DateTime StartDate { get; }
            public DateTime EndDate { get; }

            public DateRange(DateTime startDate, DateTime endDate)
            {
                StartDate = startDate;
                EndDate = endDate;
            }

            public DateTime RandomDate(Random random)
            {
                TimeSpan timeSpan = EndDate - StartDate;
                TimeSpan newSpan = new TimeSpan(0, random.Next(0, (int)timeSpan.TotalMinutes), 0);
                DateTime newDate = StartDate + newSpan;
                return newDate;
            }
        }

        public static int[] RandomDigitArray(int len)
        {
            Random rand = new Random();
            int[] RandArray = new int[len];
            for (int i = 0; i < len; i++)
                RandArray[i] = rand.Next(10);
            return RandArray;
        }
        public static int[] RandomNumberArray(int len)
        {
            Random rand = new Random();
            int[] RandArray = new int[len];
            for (int i = 0; i < len; i++)
                RandArray[i] = rand.Next();
            return RandArray;
        }
        public static string[] RandomStringArray(int len)
        {
            Random rand = new Random();
            string[] RandArray = new string[len];
            for (int i =0; i<len;i++)
                RandArray[i] = RandomString(rand, rand.Next(10));
            return RandArray;
        }
        public static DateTime[] RandomDateArray(int len)
        {
            Random rand = new Random();
            DateRange dateRange = new DateRange(new DateTime(2003, 6, 12), DateTime.Now);
            DateTime[] RandArray = new DateTime[len];
            for (int i = 0; i < len; i++)
                RandArray[i] = dateRange.RandomDate(rand);
            return RandArray;
        }

        public static int[] PartiallyShuffledDigitArray(int[] array, double p)
        {
            // Частичное перемешивание массива
            Array.Sort(array);
            int numShuffles = (int)Math.Round(p * array.Length);
            Random rand = new Random();
            for (int i = 0; i < numShuffles; i++)
            {
                int j = rand.Next(0, array.Length);
                int k = rand.Next(0, array.Length);
                SwapINT(array,j,k);
            }
            return array;
        }
        
        public static string[] PartiallyShuffledStringArray(string[] array, double p)
        {
            // Частичное перемешивание массива
            Array.Sort(array);
            int numShuffles = (int)Math.Round(p * array.Length);
            Random rand = new Random();
            for (int i = 0; i < numShuffles; i++)
            {
                int j = rand.Next(0, array.Length);
                int k = rand.Next(0, array.Length);
                SwapString(ref array[j], ref array[k]);
            }
            return array;
        }
        
        public static DateTime[] PartiallyShuffledDateArray(DateTime[] array, double p)
        {
            // Частичное перемешивание массива
            Array.Sort(array);
            int numShuffles = (int)Math.Round(p * array.Length);
            Random rand = new Random();
            for (int i = 0; i < numShuffles; i++)
            {
                int j = rand.Next(0, array.Length);
                int k = rand.Next(0, array.Length);
                SwapDate(array,j,k);
            }
            return array;
        }
        
        public static int[] UnorderedTailDigitArray(int[] arr, double percentOrdered)
        {
            Array.Sort(arr);
            int numOrdered = (int)(arr.Length * percentOrdered);
            Random rng = new Random(10);
            for (int i = numOrdered; i < arr.Length; i++)
            {
                arr[i] = rng.Next(0, 10);
            }
            return arr;
        }
        public static int[] UnorderedTailNumberArray(int[] arr, double percentOrdered)
        {
            Array.Sort(arr);
            int numOrdered = (int)(arr.Length * percentOrdered);
            Random rng = new Random(10);
            for (int i = numOrdered; i < arr.Length; i++)
            {
                arr[i] = rng.Next();
            }
            return arr;
        }
        public static string[] UnorderedTailStringArray(string[] arr, double percentOrdered)
        {
            Array.Sort(arr);
            int numOrdered = (int)(arr.Length * percentOrdered);
            Random rng = new Random(10);
            for (int i = numOrdered; i < arr.Length; i++)
            {
                arr[i] = RandomString(rng, rng.Next(10));
            }
            return arr;
        }
        public static DateTime[] UnorderedTailDateArray(DateTime[] arr, double percentOrdered)
        {
            Array.Sort(arr);
            DateRange dateRange = new DateRange(new DateTime(2003, 6, 12), DateTime.Now);
            int numOrdered = (int)(arr.Length * percentOrdered);
            Random rng = new Random();
            for (int i = numOrdered; i < arr.Length; i++)
            {
                arr[i] = dateRange.RandomDate(rng);
            }
            return arr;
        }
        
        
        public static void Main(string[] args)
        {
            //поменять все фукции на return DataTable element, чтобы тадицу заполнять инста 
            
            System.Data.DataTable DataTableOfTimDigit = new System.Data.DataTable("Сортировка массивов цифр");
            DataTableOfTimDigit.Columns.Add("Вид ", typeof(string));
            DataTableOfTimDigit.Columns.Add("N", typeof(int));
            DataTableOfTimDigit.Columns.Add("Встроенная",typeof(double));
            DataTableOfTimDigit.Columns.Add("Вставкой",typeof(double));     
            DataTableOfTimDigit.Columns.Add("Пузырьком",typeof(double));
            DataTableOfTimDigit.Columns.Add("Шейкерная",typeof(double));
            DataTableOfTimDigit.Columns.Add("Расческой",typeof(double));
            DataTableOfTimDigit.Columns.Add("Выборочная",typeof(double));
            DataTableOfTimDigit.Columns.Add("Шелла",typeof(double));
            DataTableOfTimDigit.Columns.Add("Быстрая",typeof(double));   
            DataTableOfTimDigit.Columns.Add("Слиянием",typeof(double));
            DataTableOfTimDigit.Columns.Add("Кучей",typeof(double));
            DataTableOfTimDigit.Columns.Add("Разрядная",typeof(double));
            
            System.Data.DataTable DataTableOfTimNumber = new System.Data.DataTable("Сортировка рандомных массивов цифр");
            DataTableOfTimNumber.Columns.Add("Вид ", typeof(string));
            DataTableOfTimNumber.Columns.Add("N", typeof(int));
            DataTableOfTimNumber.Columns.Add("Встроенная",typeof(double));
            DataTableOfTimNumber.Columns.Add("Вставкой",typeof(double));     
            DataTableOfTimNumber.Columns.Add("Пузырьком",typeof(double));
            DataTableOfTimNumber.Columns.Add("Шейкерная",typeof(double));
            DataTableOfTimNumber.Columns.Add("Расческой",typeof(double));
            DataTableOfTimNumber.Columns.Add("Выборочная",typeof(double));
            DataTableOfTimNumber.Columns.Add("Шелла",typeof(double));
            DataTableOfTimNumber.Columns.Add("Быстрая",typeof(double));   
            DataTableOfTimNumber.Columns.Add("Слиянием",typeof(double));
            DataTableOfTimNumber.Columns.Add("Кучей",typeof(double));
            DataTableOfTimNumber.Columns.Add("Разрядная",typeof(double));
            
            System.Data.DataTable DataTableOfTimString = new System.Data.DataTable("Сортировка рандомных массивов цифр");
            DataTableOfTimString.Columns.Add("Вид ", typeof(string));
            DataTableOfTimString.Columns.Add("N", typeof(int));
            DataTableOfTimString.Columns.Add("Встроенная",typeof(double));
            DataTableOfTimString.Columns.Add("Вставкой",typeof(double));     
            DataTableOfTimString.Columns.Add("Пузырьком",typeof(double));
            DataTableOfTimString.Columns.Add("Шейкерная",typeof(double));
            DataTableOfTimString.Columns.Add("Расческой",typeof(double));
            DataTableOfTimString.Columns.Add("Выборочная",typeof(double));
            DataTableOfTimString.Columns.Add("Шелла",typeof(double));
            DataTableOfTimString.Columns.Add("Быстрая",typeof(double));   
            DataTableOfTimString.Columns.Add("Слиянием",typeof(double));
            DataTableOfTimString.Columns.Add("Кучей",typeof(double));
            DataTableOfTimString.Columns.Add("Разрядная",typeof(double));
            
            System.Data.DataTable DataTableOfTimDate = new System.Data.DataTable("Сортировка рандомных массивов цифр");
            DataTableOfTimDate.Columns.Add("Вид ", typeof(string));
            DataTableOfTimDate.Columns.Add("N", typeof(int));
            DataTableOfTimDate.Columns.Add("Встроенная",typeof(double));
            DataTableOfTimDate.Columns.Add("Вставкой",typeof(double));     
            DataTableOfTimDate.Columns.Add("Пузырьком",typeof(double));
            DataTableOfTimDate.Columns.Add("Шейкерная",typeof(double));
            DataTableOfTimDate.Columns.Add("Расческой",typeof(double));
            DataTableOfTimDate.Columns.Add("Выборочная",typeof(double));
            DataTableOfTimDate.Columns.Add("Шелла",typeof(double));
            DataTableOfTimDate.Columns.Add("Быстрая",typeof(double));   
            DataTableOfTimDate.Columns.Add("Слиянием",typeof(double));
            DataTableOfTimDate.Columns.Add("Кучей",typeof(double));
            DataTableOfTimDate.Columns.Add("Разрядная",typeof(double));

            int[] RandomDigit50 = RandomDigitArray(50);
            int[] RandomDigit500 = RandomDigitArray(500);
            int[] RandomDigit5000 = RandomDigitArray(5000);
            int[] RandomDigit50000 = RandomDigitArray(50000);
            int[] RandomDigit500000 = RandomDigitArray(500000);
            
            int[] PartiallyShuffledDigit50 = PartiallyShuffledDigitArray(RandomDigit50, 0.25);
            int[] PartiallyShuffledDigit500 = PartiallyShuffledDigitArray(RandomDigit500, 0.25);
            int[] PartiallyShuffledDigit5000 = PartiallyShuffledDigitArray(RandomDigit5000, 0.25);
            int[] PartiallyShuffledDigit50000 = PartiallyShuffledDigitArray(RandomDigit50000, 0.25);
            int[] PartiallyShuffledDigit500000 = PartiallyShuffledDigitArray(RandomDigit500000, 0.25);

            int[] UnorderedTailDigit50 = UnorderedTailDigitArray(RandomDigit50, 0.25);
            int[] UnorderedTailDigit500 = UnorderedTailDigitArray(RandomDigit500, 0.25);
            int[] UnorderedTailDigit5000 = UnorderedTailDigitArray(RandomDigit5000, 0.25);
            int[] UnorderedTailDigit50000 = UnorderedTailDigitArray(RandomDigit50000, 0.25);
            int[] UnorderedTailDigit500000 = UnorderedTailDigitArray(RandomDigit500000, 0.25);
            
            int[] RandomNumber50 = RandomNumberArray(50);
            int[] RandomNumber500 = RandomNumberArray(500);
            int[] RandomNumber5000 = RandomNumberArray(5000);
            int[] RandomNumber50000 = RandomNumberArray(50000);
            int[] RandomNumber500000 = RandomNumberArray(500000);

            int[] PartiallyShuffledNumber50 = PartiallyShuffledDigitArray(RandomNumber50, 0.25);
            int[] PartiallyShuffledNumber500 = PartiallyShuffledDigitArray(RandomNumber500, 0.25);
            int[] PartiallyShuffledNumber5000 = PartiallyShuffledDigitArray(RandomNumber5000, 0.25);
            int[] PartiallyShuffledNumber50000 = PartiallyShuffledDigitArray(RandomNumber50000, 0.25);
            int[] PartiallyShuffledNumber500000 = PartiallyShuffledDigitArray(RandomNumber500000, 0.25);
            
            int[] UnorderedTailNumber50 = UnorderedTailNumberArray(RandomNumber50, 0.25);
            int[] UnorderedTailNumber500 = UnorderedTailNumberArray(RandomNumber500, 0.25);
            int[] UnorderedTailNumber5000 = UnorderedTailNumberArray(RandomNumber5000, 0.25);
            int[] UnorderedTailNumber50000 = UnorderedTailNumberArray(RandomNumber50000, 0.25);
            int[] UnorderedTailNumber500000 = UnorderedTailNumberArray(RandomNumber500000, 0.25);

            string[] RandomString50 = RandomStringArray(50);
            string[] RandomString500 = RandomStringArray(500);
            string[] RandomString5000 = RandomStringArray(5000);
            string[] RandomString50000 = RandomStringArray(50000);
            string[] RandomString500000 = RandomStringArray(500000);

            string[] PartiallyShuffledString50 = PartiallyShuffledStringArray(RandomString50, 0.25);
            string[] PartiallyShuffledString500 = PartiallyShuffledStringArray(RandomString500, 0.25);
            string[] PartiallyShuffledString5000 = PartiallyShuffledStringArray(RandomString5000, 0.25);
            string[] PartiallyShuffledString50000 = PartiallyShuffledStringArray(RandomString50000, 0.25);
            string[] PartiallyShuffledString500000 = PartiallyShuffledStringArray(RandomString500000, 0.25);
            
            string[] UnorderedTailString50 = UnorderedTailStringArray(RandomString50, 0.25);
            string[] UnorderedTailString500 = UnorderedTailStringArray(RandomString500, 0.25);
            string[] UnorderedTailString5000 = UnorderedTailStringArray(RandomString5000, 0.25);
            string[] UnorderedTailString50000 = UnorderedTailStringArray(RandomString50000, 0.25);
            string[] UnorderedTailString500000 = UnorderedTailStringArray(RandomString500000, 0.25);

            DateTime[] RandomDate50 = RandomDateArray(50);
            DateTime[] RandomDate500 = RandomDateArray(500);
            DateTime[] RandomDate5000 = RandomDateArray(5000);
            DateTime[] RandomDate50000 = RandomDateArray(50000);
            DateTime[] RandomDate500000 = RandomDateArray(500000);
            
            DateTime[] PartiallyShuffledDate50 = PartiallyShuffledDateArray(RandomDate50, 0.25);
            DateTime[] PartiallyShuffledDate500 = PartiallyShuffledDateArray(RandomDate500, 0.25);
            DateTime[] PartiallyShuffledDate5000 = PartiallyShuffledDateArray(RandomDate5000, 0.25);
            DateTime[] PartiallyShuffledDate50000 = PartiallyShuffledDateArray(RandomDate50000, 0.25);
            DateTime[] PartiallyShuffledDate500000 = PartiallyShuffledDateArray(RandomDate500000, 0.25);
            
            DateTime[] UnorderedTailDate50 = UnorderedTailDateArray(RandomDate50, 0.25);
            DateTime[] UnorderedTailDate500 = UnorderedTailDateArray(RandomDate500, 0.25);
            DateTime[] UnorderedTailDate5000 = UnorderedTailDateArray(RandomDate5000, 0.25);
            DateTime[] UnorderedTailDate50000 = UnorderedTailDateArray(RandomDate50000, 0.25);
            DateTime[] UnorderedTailDate500000 = UnorderedTailDateArray(RandomDate500000, 0.25);

            Console.WriteLine("Рандомные массивы цифр:");
            resultDigit(RandomDigit50,RandomDigit500,RandomDigit5000,RandomDigit50000,RandomDigit500000, DataTableOfTimDigit, "Random");
            Console.WriteLine("\n==============================\n");
            Console.WriteLine("Рандомные массивы чисел:");
            resultDigit(RandomNumber50,RandomNumber500,RandomNumber5000,RandomNumber50000,RandomNumber500000, DataTableOfTimNumber, "Random");
            Console.WriteLine("\n==============================\n");
            Console.WriteLine("Рандомные массивы строк:");
            resultString(RandomString50,RandomString500,RandomString5000,RandomString50000,RandomString500000, DataTableOfTimString ,"Random");
            Console.WriteLine("\n==============================\n");
            Console.WriteLine("Рандомные массивы структур:");
            resultDate(RandomDate50, RandomDate500, RandomDate5000, RandomDate50000, RandomDate500000, DataTableOfTimDate ,"Random");
            Console.WriteLine("\n==============================\n");
            
            Console.WriteLine("Частично перемешанные массивы цифр:");
            resultDigit(PartiallyShuffledDigit50,PartiallyShuffledDigit500,PartiallyShuffledDigit5000,PartiallyShuffledDigit50000,PartiallyShuffledDigit500000, DataTableOfTimDigit, "Shuffle");
            Console.WriteLine("\n==============================\n");
            Console.WriteLine("Частично перемешанные массивы чисел:");
            resultDigit(PartiallyShuffledNumber50,PartiallyShuffledNumber500,PartiallyShuffledNumber5000,PartiallyShuffledNumber50000,PartiallyShuffledNumber500000, DataTableOfTimDigit, "Shuffle");
            Console.WriteLine("\n==============================\n");
            Console.WriteLine("Частично перемешанные массивы строк:");
            resultString(PartiallyShuffledString50,PartiallyShuffledString500,PartiallyShuffledString5000,PartiallyShuffledString50000,PartiallyShuffledString500000, DataTableOfTimString, "Shuffle");
            Console.WriteLine("\n==============================\n");
            Console.WriteLine("Частично перемешанные массивы структур:");
            resultDate(PartiallyShuffledDate50, PartiallyShuffledDate500,PartiallyShuffledDate5000,PartiallyShuffledDate50000,PartiallyShuffledDate500000, DataTableOfTimDate, "Shuffle");
            Console.WriteLine("\n==============================\n");
            
            Console.WriteLine("\"Неупорядоченный хвост\" массивы цифр:");
            resultDigit(UnorderedTailDigit50,UnorderedTailDigit500,UnorderedTailDigit5000,UnorderedTailDigit50000,UnorderedTailDigit500000, DataTableOfTimDigit, "Tail");
            Console.WriteLine("\n==============================\n");
            Console.WriteLine("\"Неупорядоченный хвост\" массивы чисел:");
            resultDigit(UnorderedTailNumber50,UnorderedTailNumber500,UnorderedTailNumber5000,UnorderedTailNumber50000,UnorderedTailNumber500000, DataTableOfTimDigit, "Tail");
            Console.WriteLine("\n==============================\n");
            Console.WriteLine("\"Неупорядоченный хвост\" массивы строк:");
            resultString(UnorderedTailString50,UnorderedTailString500,UnorderedTailString5000,UnorderedTailString50000,UnorderedTailString500000, DataTableOfTimString, "Tail");
            Console.WriteLine("\n==============================\n");
            Console.WriteLine("\"Неупорядоченный хвост\" массивы структур:");
            resultDate(UnorderedTailDate50,UnorderedTailDate500,UnorderedTailDate5000,UnorderedTailDate50000,UnorderedTailDate500000,DataTableOfTimDate, "Tail");
            Console.WriteLine("\n==============================\n");

            ViewDataTable(DataTableOfTimDigit);
            ViewDataTable(DataTableOfTimNumber);
            ViewDataTable(DataTableOfTimString);
            ViewDataTable(DataTableOfTimDate);

            //ExportDataTableToExcel(DataTableOfTimDigit,"D//");
            //ExportDataTableToExcel(DataTableOfTimNumber,"D//");
            //ExportDataTableToExcel(DataTableOfTimString,"D//");
            //ExportDataTableToExcel(DataTableOfTimDate, "D//");


        }
        
        static public void ExportDataTableToExcel(System.Data.DataTable dataTable, string fileName)
        {
            //filename - директория хранения эксель файла   
            // Создаем приложение Excel
            var excel = new Application();
            excel.Visible = false;
            excel.DisplayAlerts = false;

            // Создаем новую книгу Excel
            var workbook = excel.Workbooks.Add(Type.Missing);
            var worksheet = (Worksheet)workbook.ActiveSheet;

            // Заполняем лист Excel заголовками столбцов
            var columns = dataTable.Columns;
            var colIndex = 1;
            foreach (DataColumn column in columns)
            {
                worksheet.Cells[1, colIndex] = column.ColumnName;
                colIndex++;
            }

            // Заполняем лист Excel данными из DataTable
            var rows = dataTable.Rows;
            var rowIndex = 2;
            foreach (DataRow row in rows)
            {
                colIndex = 1;
                foreach (DataColumn column in columns)
                {
                    worksheet.Cells[rowIndex, colIndex] = row[column].ToString();
                    colIndex++;
                }
                rowIndex++;
            }

            // Сохраняем книгу Excel и закрываем приложение
            workbook.SaveAs(fileName);
            workbook.Close();
            excel.Quit();
        }
        
        
        
        static public void ViewDataTable(System.Data.DataTable table)
        {
            bool firstRow = true;
            Console.Write(table.TableName + " \n");
            foreach (DataRow row in table.Rows)
            {
                if (firstRow)
                {
                    foreach (DataColumn column in table.Columns)
                    {
                        Console.Write(column.ColumnName + " ");
                    }
                    Console.WriteLine();
                    firstRow = false;
                }
                foreach (DataColumn column in table.Columns)
                {
                    Console.Write(row[column].ToString() + " ");
                }
                Console.WriteLine();
            }

        }

        static void resultDigit(int[] SG50, int[] SG500, int[] SG5000, int[] SG50000, int[] SG500000, System.Data.DataTable DataTableOfTimDigit, string way)
        {
            Stopwatch stopwatch = new Stopwatch();
            Stopwatch stopwatchQuick = new Stopwatch();
            Stopwatch stopwatchMerge = new Stopwatch();

            stopwatch.Start();
            Array.Sort(SG50);
            stopwatch.Stop();
            
            stopwatchQuick.Start();
            QuickSortDigit(SG50, 0, SG50.Length - 1);
            stopwatchQuick.Stop();
            
            stopwatchMerge.Start();
            MergeSortDigit(SG50, 0, SG50.Length - 1);
            stopwatchMerge.Stop();

            DataTableOfTimDigit.Rows.Add(way, SG50.Length, stopwatch.Elapsed.TotalMilliseconds, InsertionSortDigit(SG50),  BubbleSortDigit(SG50), ShakerSortDigit(SG50), CombSortDigit(SG50), SelectionSortDigit(SG50), ShellSortDigit(SG50), stopwatchQuick.Elapsed.TotalMilliseconds, stopwatchMerge.Elapsed.TotalMilliseconds, HeapSortDigit(SG50, SG50.Length - 1), RadixSortDigit(SG50));
            
            stopwatch.Reset();
            stopwatchQuick.Reset();
            stopwatchMerge.Reset();
            
            // =================================== //
            
            stopwatch.Start();
            Array.Sort(SG50);
            stopwatch.Stop();
            
            stopwatchQuick.Start();
            QuickSortDigit(SG500, 0, SG500.Length - 1);
            stopwatchQuick.Stop();
            
            stopwatchMerge.Start();
            MergeSortDigit(SG500, 0, SG500.Length - 1);
            stopwatchMerge.Stop();

            DataTableOfTimDigit.Rows.Add(way, SG500.Length, stopwatch.Elapsed.TotalMilliseconds, InsertionSortDigit(SG500),  BubbleSortDigit(SG500), ShakerSortDigit(SG500), CombSortDigit(SG500), SelectionSortDigit(SG500), ShellSortDigit(SG500), stopwatchQuick.Elapsed.TotalMilliseconds, stopwatchMerge.Elapsed.TotalMilliseconds, HeapSortDigit(SG500, SG500.Length - 1), RadixSortDigit(SG500));
            
            stopwatch.Reset();
            stopwatchQuick.Reset();
            stopwatchMerge.Reset();
            
            // =================================== //
            
            stopwatch.Start();
            Array.Sort(SG5000);
            stopwatch.Stop();
            
            stopwatchQuick.Start();
            QuickSortDigit(SG5000, 0, SG5000.Length - 1);
            stopwatchQuick.Stop();
            
            stopwatchMerge.Start();
            MergeSortDigit(SG5000, 0, SG5000.Length - 1);
            stopwatchMerge.Stop();

            DataTableOfTimDigit.Rows.Add(way, SG5000.Length, stopwatch.Elapsed.TotalMilliseconds, InsertionSortDigit(SG5000),  BubbleSortDigit(SG5000), ShakerSortDigit(SG5000), CombSortDigit(SG5000), SelectionSortDigit(SG5000), ShellSortDigit(SG5000), stopwatchQuick.Elapsed.TotalMilliseconds, stopwatchMerge.Elapsed.TotalMilliseconds, HeapSortDigit(SG5000, SG5000.Length - 1), RadixSortDigit(SG5000));
            
            stopwatch.Reset();
            stopwatchQuick.Reset();
            stopwatchMerge.Reset();
            
            // =================================== //
            
            stopwatch.Start();
            Array.Sort(SG50000);
            stopwatch.Stop();
            
            stopwatchQuick.Start();
            QuickSortDigit(SG50000, 0, SG50000.Length - 1);
            stopwatchQuick.Stop();
            
            stopwatchMerge.Start();
            MergeSortDigit(SG50000, 0, SG50000.Length - 1);
            stopwatchMerge.Stop();

            DataTableOfTimDigit.Rows.Add(way, SG50000.Length, stopwatch.Elapsed.TotalMilliseconds, InsertionSortDigit(SG50000),  BubbleSortDigit(SG50000), ShakerSortDigit(SG50000), CombSortDigit(SG50000), SelectionSortDigit(SG50000), ShellSortDigit(SG50000), stopwatchQuick.Elapsed.TotalMilliseconds, stopwatchMerge.Elapsed.TotalMilliseconds, HeapSortDigit(SG50000, SG50000.Length - 1), RadixSortDigit(SG50000));
            
            stopwatch.Reset();
            stopwatchQuick.Reset();
            stopwatchMerge.Reset();
            
            // =================================== //
            
            stopwatch.Start();
            Array.Sort(SG500000);
            stopwatch.Stop();
            
            stopwatchQuick.Start();
            QuickSortDigit(SG500000, 0, SG500000.Length - 1);
            stopwatchQuick.Stop();
            
            stopwatchMerge.Start();
            MergeSortDigit(SG500000, 0, SG500000.Length - 1);
            stopwatchMerge.Stop();

            DataTableOfTimDigit.Rows.Add(way, SG500000.Length, stopwatch.Elapsed.TotalMilliseconds, InsertionSortDigit(SG500000),  BubbleSortDigit(SG500000), ShakerSortDigit(SG500000), CombSortDigit(SG500000), SelectionSortDigit(SG500000), ShellSortDigit(SG500000), stopwatchQuick.Elapsed.TotalMilliseconds, stopwatchMerge.Elapsed.TotalMilliseconds, HeapSortDigit(SG500000, SG500000.Length - 1), RadixSortDigit(SG500000));
            
            stopwatch.Reset();
            stopwatchQuick.Reset();
            stopwatchMerge.Reset();
            
            // =================================== //
        }

        static void resultString(string[] s1, string[] s2, string[] s3, string[] s4, string[] s5, System.Data.DataTable DataTableOfTimDigit, string way)
        {
            
            
            Stopwatch stopwatch = new Stopwatch();
            Stopwatch stopwatchQuick = new Stopwatch();
            Stopwatch stopwatchMerge = new Stopwatch();

            stopwatch.Start();
            Array.Sort(s1);
            stopwatch.Stop();
            
            stopwatchQuick.Start();
            QuickSortString(s1, 0, s1.Length - 1);
            stopwatchQuick.Stop();
            
            stopwatchMerge.Start();
            MergeSortString(s1);
            stopwatchMerge.Stop();

            DataTableOfTimDigit.Rows.Add(way, s1.Length, stopwatch.Elapsed.TotalMilliseconds, InsertionSortString(s1),  BubbleSortString(s1), ShakerSortString(s1), CombSortString(s1), SelectionSortString(s1), ShellSortString(s1), stopwatchQuick.Elapsed.TotalMilliseconds, stopwatchMerge.Elapsed.TotalMilliseconds, HeapSortString(s1), RadixSortString(s1));
            
            stopwatch.Reset();
            stopwatchQuick.Reset();
            stopwatchMerge.Reset();
            
            // =================================== //
            
            stopwatch.Start();
            Array.Sort(s2);
            stopwatch.Stop();
            
            stopwatchQuick.Start();
            QuickSortString(s2, 0, s2.Length - 1);
            stopwatchQuick.Stop();
            
            stopwatchMerge.Start();
            MergeSortString(s2);
            stopwatchMerge.Stop();

            DataTableOfTimDigit.Rows.Add(way, s2.Length, stopwatch.Elapsed.TotalMilliseconds, InsertionSortString(s2),  BubbleSortString(s2), ShakerSortString(s2), CombSortString(s2), SelectionSortString(s2), ShellSortString(s2), stopwatchQuick.Elapsed.TotalMilliseconds, stopwatchMerge.Elapsed.TotalMilliseconds, HeapSortString(s2), RadixSortString(s2));
            
            stopwatch.Reset();
            stopwatchQuick.Reset();
            stopwatchMerge.Reset();
            
            // =================================== //
            
            stopwatch.Start();
            Array.Sort(s3);
            stopwatch.Stop();
            
            stopwatchQuick.Start();
            QuickSortString(s3, 0, s3.Length - 1);
            stopwatchQuick.Stop();
            
            stopwatchMerge.Start();
            MergeSortString(s3);
            stopwatchMerge.Stop();

            DataTableOfTimDigit.Rows.Add(way, s3.Length, stopwatch.Elapsed.TotalMilliseconds, InsertionSortString(s3),  BubbleSortString(s3), ShakerSortString(s3), CombSortString(s3), SelectionSortString(s3), ShellSortString(s3), stopwatchQuick.Elapsed.TotalMilliseconds, stopwatchMerge.Elapsed.TotalMilliseconds, HeapSortString(s3), RadixSortString(s3));
            
            stopwatch.Reset();
            stopwatchQuick.Reset();
            stopwatchMerge.Reset();
            
            // =================================== //
            
            stopwatch.Start();
            Array.Sort(s4);
            stopwatch.Stop();
            
            stopwatchQuick.Start();
            QuickSortString(s4, 0, s4.Length - 1);
            stopwatchQuick.Stop();
            
            stopwatchMerge.Start();
            MergeSortString(s4);
            stopwatchMerge.Stop();

            DataTableOfTimDigit.Rows.Add(way, s4.Length, stopwatch.Elapsed.TotalMilliseconds, InsertionSortString(s4),  BubbleSortString(s4), ShakerSortString(s4), CombSortString(s4), SelectionSortString(s4), ShellSortString(s4), stopwatchQuick.Elapsed.TotalMilliseconds, stopwatchMerge.Elapsed.TotalMilliseconds, HeapSortString(s4), RadixSortString(s4));
            
            stopwatch.Reset();
            stopwatchQuick.Reset();
            stopwatchMerge.Reset();
            
            // =================================== //
            
            stopwatch.Start();
            Array.Sort(s5);
            stopwatch.Stop();
            
            stopwatchQuick.Start();
            QuickSortString(s5, 0, s5.Length - 1);
            stopwatchQuick.Stop();
            
            stopwatchMerge.Start();
            MergeSortString(s5);
            stopwatchMerge.Stop();

            DataTableOfTimDigit.Rows.Add(way, s5.Length, stopwatch.Elapsed.TotalMilliseconds, InsertionSortString(s5),  BubbleSortString(s5), ShakerSortString(s5), CombSortString(s5), SelectionSortString(s5), ShellSortString(s5), stopwatchQuick.Elapsed.TotalMilliseconds, stopwatchMerge.Elapsed.TotalMilliseconds, HeapSortString(s5), RadixSortString(s5));
            
            stopwatch.Reset();
            stopwatchQuick.Reset();
            stopwatchMerge.Reset();
            
            // =================================== //
            
        }

        static void resultDate(DateTime[] s1, DateTime[] s2, DateTime[] s3, DateTime[] s4, DateTime[] s5, System.Data.DataTable DataTableOfTimDigit, string way)
        {
           
            Stopwatch stopwatch = new Stopwatch();
            Stopwatch stopwatchQuick = new Stopwatch();
            Stopwatch stopwatchMerge = new Stopwatch();

            stopwatch.Start();
            Array.Sort(s1);
            stopwatch.Stop();
            
            stopwatchQuick.Start();
            QuickSortDate(s1, 0, s1.Length - 1);
            stopwatchQuick.Stop();
            
            stopwatchMerge.Start();
            MergeSortDate(s1, 0, s1.Length - 1);
            stopwatchMerge.Stop();

            DataTableOfTimDigit.Rows.Add(way, s1.Length, stopwatch.Elapsed.TotalMilliseconds, InsertionSortDate(s1),  BubbleSortDate(s1), ShakerSortDate(s1), CombSortDate(s1), SelectionSortDate(s1), ShellSortDate(s1), stopwatchQuick.Elapsed.TotalMilliseconds, stopwatchMerge.Elapsed.TotalMilliseconds, HeapSortDate(s1, s1.Length - 1), RadixSortDate(s1));
            
            stopwatch.Reset();
            stopwatchQuick.Reset();
            stopwatchMerge.Reset();
            
            // =================================== //
            
            stopwatch.Start();
            Array.Sort(s2);
            stopwatch.Stop();
            
            stopwatchQuick.Start();
            QuickSortDate(s2, 0, s2.Length - 1);
            stopwatchQuick.Stop();
            
            stopwatchMerge.Start();
            MergeSortDate(s2, 0, s2.Length - 1);
            stopwatchMerge.Stop();

            DataTableOfTimDigit.Rows.Add(way, s2.Length, stopwatch.Elapsed.TotalMilliseconds, InsertionSortDate(s2),  BubbleSortDate(s2), ShakerSortDate(s2), CombSortDate(s2), SelectionSortDate(s2), ShellSortDate(s2), stopwatchQuick.Elapsed.TotalMilliseconds, stopwatchMerge.Elapsed.TotalMilliseconds, HeapSortDate(s2, s2.Length - 1), RadixSortDate(s2));
            
            stopwatch.Reset();
            stopwatchQuick.Reset();
            stopwatchMerge.Reset();
            
            // =================================== //
            
            stopwatch.Start();
            Array.Sort(s3);
            stopwatch.Stop();
            
            stopwatchQuick.Start();
            QuickSortDate(s3, 0, s3.Length - 1);
            stopwatchQuick.Stop();
            
            stopwatchMerge.Start();
            MergeSortDate(s3, 0, s3.Length - 1);
            stopwatchMerge.Stop();

            DataTableOfTimDigit.Rows.Add(way, s3.Length, stopwatch.Elapsed.TotalMilliseconds, InsertionSortDate(s3),  BubbleSortDate(s3), ShakerSortDate(s3), CombSortDate(s3), SelectionSortDate(s3), ShellSortDate(s3), stopwatchQuick.Elapsed.TotalMilliseconds, stopwatchMerge.Elapsed.TotalMilliseconds, HeapSortDate(s3, s3.Length - 1), RadixSortDate(s3));
            
            stopwatch.Reset();
            stopwatchQuick.Reset();
            stopwatchMerge.Reset();
            
            // =================================== //
            
            stopwatch.Start();
            Array.Sort(s4);
            stopwatch.Stop();
            
            stopwatchQuick.Start();
            QuickSortDate(s4, 0, s4.Length - 1);
            stopwatchQuick.Stop();
            
            stopwatchMerge.Start();
            MergeSortDate(s4, 0, s4.Length - 1);
            stopwatchMerge.Stop();

            DataTableOfTimDigit.Rows.Add(way, s4.Length, stopwatch.Elapsed.TotalMilliseconds, InsertionSortDate(s4),  BubbleSortDate(s4), ShakerSortDate(s4), CombSortDate(s4), SelectionSortDate(s4), ShellSortDate(s4), stopwatchQuick.Elapsed.TotalMilliseconds, stopwatchMerge.Elapsed.TotalMilliseconds, HeapSortDate(s4, s4.Length - 1), RadixSortDate(s4));
            
            stopwatch.Reset();
            stopwatchQuick.Reset();
            stopwatchMerge.Reset();
            
            // =================================== //

            stopwatch.Start();
            Array.Sort(s5);
            stopwatch.Stop();
            
            stopwatchQuick.Start();
            QuickSortDate(s5, 0, s5.Length - 1);
            stopwatchQuick.Stop();
            
            stopwatchMerge.Start();
            MergeSortDate(s5, 0, s5.Length - 1);
            stopwatchMerge.Stop();

            DataTableOfTimDigit.Rows.Add(way, s5.Length, stopwatch.Elapsed.TotalMilliseconds, InsertionSortDate(s5),  BubbleSortDate(s5), ShakerSortDate(s5), CombSortDate(s5), SelectionSortDate(s5), ShellSortDate(s5), stopwatchQuick.Elapsed.TotalMilliseconds, stopwatchMerge.Elapsed.TotalMilliseconds, HeapSortDate(s5, s5.Length - 1), RadixSortDate(s5));
            
            stopwatch.Reset();
            stopwatchQuick.Reset();
            stopwatchMerge.Reset();
            
            // =================================== //
        }

        static string RandomString(Random random, int length)
        {
            const string chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
            return new string(Enumerable.Repeat(chars, length).Select(s => s[random.Next(s.Length)]).ToArray());
        }

        private static void SwapINT(int[] array, int i, int j)
        {
            int temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        }
        private static void SwapString(ref string a, ref string b)
        {
            string temp = a;
            a = b;
            b = temp;
        }

        private static void SwapDate(DateTime[] array, int i, int j)
        {
            DateTime temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        }

        //сортировка вставками
        static double InsertionSortDigit(int[] inArray)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            int x;
            int j;
            for (int i = 1; i < inArray.Length; i++)
            {
                x = inArray[i];
                j = i;
                while (j > 0 && inArray[j - 1] > x)
                {
                    SwapINT(inArray, j, j - 1);
                    j -= 1;
                }

                inArray[j] = x;
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        static double InsertionSortString(string[] array)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            for (int i = 1; i < array.Length; i++)
            {
                string key = array[i];
                int j = i - 1;
                while (j >= 0 && string.Compare(array[j], key) > 0)
                {
                    array[j + 1] = array[j];
                    j = j - 1;
                }

                array[j + 1] = key;
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        static double InsertionSortDate(DateTime[] inArray)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            DateTime x;
            int j;
            for (int i = 1; i < inArray.Length; i++)
            {
                x = inArray[i];
                j = i;
                while (j > 0 && inArray[j - 1] > x)
                {
                    SwapDate(inArray, j, j - 1);
                    j -= 1;
                }

                inArray[j] = x;
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        //сортировка шейкерная
        static double ShakerSortDigit(int[] inArray)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            int left = 0,
                right = inArray.Length - 1;
            while (left < right)
            {
                for (int i = left; i < right; i++)
                {
                    if (inArray[i] > inArray[i + 1])
                        SwapINT(inArray, i, i + 1);
                }

                right--;
                for (int i = right; i > left; i--)
                {
                    if (inArray[i - 1] > inArray[i])
                        SwapINT(inArray, i - 1, i);
                }

                left++;
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        static double ShakerSortString(string[] arr)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            bool swapped = true;
            int start = 0;
            int end = arr.Length - 1;

            while (swapped)
            {
                // Reset the flag to check if any swapping occurred in this iteration
                swapped = false;

                // Perform a bubble sort from left to right
                for (int i = start; i < end; i++)
                {
                    if (string.Compare(arr[i], arr[i + 1]) > 0)
                    {
                        SwapString(ref arr[i], ref arr[i + 1]);
                        swapped = true;
                    }
                }

                // If no swapping occurred in the first iteration, the array is already sorted
                if (!swapped)
                    break;

                // Move the end index one position to the left
                end--;

                // Perform a bubble sort from right to left
                for (int i = end - 1; i >= start; i--)
                {
                    if (string.Compare(arr[i], arr[i + 1]) > 0)
                    {
                        SwapString(ref arr[i], ref arr[i + 1]);
                        swapped = true;
                    }
                }

                // Move the start index one position to the right
                start++;
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        static double ShakerSortDate(DateTime[] inArray)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            int left = 0, right = inArray.Length - 1;
            while (left < right)
            {
                for (int i = left; i < right; i++)
                {
                    if (inArray[i] > inArray[i + 1])
                        SwapDate(inArray, i, i + 1);
                }

                right--;
                for (int i = right; i > left; i--)
                {
                    if (inArray[i - 1] > inArray[i])
                        SwapDate(inArray, i - 1, i);
                }

                left++;
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        //сортировка расческой
        public static double CombSortDigit(int[] input)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            double gap = input.Length;
            bool swaps = true;
            while (gap > 1 || swaps)
            {
                gap /= 1.247330950103979;
                if (gap < 1)
                {
                    gap = 1;
                }

                int i = 0;
                swaps = false;
                while (i + gap < input.Length)
                {
                    int igap = i + (int)gap;
                    if (input[i] > input[igap])
                    {
                        int swap = input[i];
                        input[i] = input[igap];
                        input[igap] = swap;
                        swaps = true;
                    }

                    i++;
                }
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        public static double CombSortString(string[] arr)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            int gap = arr.Length;
            bool swapped = true;

            while (gap > 1 || swapped)
            {
                gap = (gap * 10) / 13;
                if (gap < 1)
                    gap = 1;

                swapped = false;
                for (int i = 0; i < arr.Length - gap; i++)
                {
                    if (string.Compare(arr[i], arr[i + gap]) > 0)
                    {
                        string temp = arr[i];
                        arr[i] = arr[i + gap];
                        arr[i + gap] = temp;
                        swapped = true;
                    }
                }
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        public static double CombSortDate(DateTime[] input)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            double gap = input.Length;
            bool swaps = true;
            while (gap > 1 || swaps)
            {
                gap /= 1.247330950103979;
                if (gap < 1)
                {
                    gap = 1;
                }

                int i = 0;
                swaps = false;
                while (i + gap < input.Length)
                {
                    int igap = i + (int)gap;
                    if (input[i] > input[igap])
                    {
                        DateTime swap = input[i];
                        input[i] = input[igap];
                        input[igap] = swap;
                        swaps = true;
                    }

                    i++;
                }
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        //сортировка пузырьком
        static double BubbleSortDigit(int[] inArray)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            for (int i = 0; i < inArray.Length; i++)
            {
                for (int j = 0; j < inArray.Length - i - 1; j++)
                {
                    if (inArray[j] > inArray[j + 1])
                    {
                        int temp = inArray[j];
                        inArray[j] = inArray[j + 1];
                        inArray[j + 1] = temp;
                    }
                }
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        static double BubbleSortString(string[] arr)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            int n = arr.Length;
            for (int i = 0; i < n - 1; i++)
            {
                for (int j = 0; j < n - i - 1; j++)
                {
                    if (arr[j].CompareTo(arr[j + 1]) > 0)
                    {
                        // Меняем элементы местами
                        string temp = arr[j];
                        arr[j] = arr[j + 1];
                        arr[j + 1] = temp;
                    }
                }
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        static double BubbleSortDate(DateTime[] array)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            for (int i = 0; i < array.Length - 1; i++)
            {
                for (int j = 0; j < array.Length - i - 1; j++)
                {
                    if (array[j] > array[j + 1])
                    {
                        // Обмен местами текущего элемента со следующим элементом
                        DateTime temp = array[j];
                        array[j] = array[j + 1];
                        array[j + 1] = temp;
                    }
                }
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        //сортировка выбором
        static double SelectionSortDigit(int[] inArray)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            //intArray - это массив целых чисел
            int indx; //переменная для хранения индекса минимального элемента массива
            for (int i = 0; i < inArray.Length; i++) //проходим по массиву с начала и до конца
            {
                indx = i; //считаем, что минимальный элемент имеет текущий индекс 
                for (int j = i; j < inArray.Length; j++) //ищем минимальный элемент в неотсортированной части
                {
                    if (inArray[j] < inArray[indx])
                    {
                        indx = j; //нашли в массиве число меньше, чем intArray[indx] - запоминаем его индекс в массиве
                    }
                }

                if (inArray[indx] == inArray[i]) //если минимальный элемент равен текущему значению - ничего не меняем
                    continue;
                //меняем местами минимальный элемент и первый в неотсортированной части
                int temp = inArray[i]; //временная переменная, чтобы не потерять значение intArray[i]
                inArray[i] = inArray[indx];
                inArray[indx] = temp;
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        public static double SelectionSortString(string[] arr)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            int n = arr.Length;
            for (int i = 0; i < n - 1; i++)
            {
                int minIndex = i;
                for (int j = i + 1; j < n; j++)
                {
                    if (arr[j].CompareTo(arr[minIndex]) < 0)
                    {
                        minIndex = j;
                    }
                }

                if (minIndex != i)
                {
                    string temp = arr[i];
                    arr[i] = arr[minIndex];
                    arr[minIndex] = temp;
                }
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        static double SelectionSortDate(DateTime[] inArray)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            //intArray - это массив целых чисел
            int indx; //переменная для хранения индекса минимального элемента массива
            for (int i = 0; i < inArray.Length; i++) //проходим по массиву с начала и до конца
            {
                indx = i; //считаем, что минимальный элемент имеет текущий индекс 
                for (int j = i; j < inArray.Length; j++) //ищем минимальный элемент в неотсортированной части
                {
                    if (inArray[j] < inArray[indx])
                    {
                        indx = j; //нашли в массиве число меньше, чем intArray[indx] - запоминаем его индекс в массиве
                    }
                }

                if (inArray[indx] == inArray[i]) //если минимальный элемент равен текущему значению - ничего не меняем
                    continue;
                //меняем местами минимальный элемент и первый в неотсортированной части
                DateTime temp = inArray[i]; //временная переменная, чтобы не потерять значение intArray[i]
                inArray[i] = inArray[indx];
                inArray[indx] = temp;
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        //сортировка Шелла
        static double ShellSortDigit(int[] arr)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            int j;
            int step = arr.Length / 2;
            while (step > 0)
            {
                for (int i = 0; i < (arr.Length - step); i++)
                {
                    j = i;
                    while ((j >= 0) && (arr[j] > arr[j + step]))
                    {
                        int tmp = arr[j];
                        arr[j] = arr[j + step];
                        arr[j + step] = tmp;
                        j -= step;
                    }
                }

                step = step / 2;
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        static double ShellSortString(string[] arr)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            int n = arr.Length;
            int gap = n / 2;

            while (gap > 0)
            {
                for (int i = gap; i < n; i++)
                {
                    string temp = arr[i];
                    int j = i;

                    while (j >= gap && string.Compare(arr[j - gap], temp) > 0)
                    {
                        arr[j] = arr[j - gap];
                        j -= gap;
                    }

                    arr[j] = temp;
                }

                gap /= 2;
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        static double ShellSortDate(DateTime[] arr)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            int j;
            int step = arr.Length / 2;
            while (step > 0)
            {
                for (int i = 0; i < (arr.Length - step); i++)
                {
                    j = i;
                    while ((j >= 0) && (arr[j] > arr[j + step]))
                    {
                        DateTime tmp = arr[j];
                        arr[j] = arr[j + step];
                        arr[j + step] = tmp;
                        j -= step;
                    }
                }

                step = step / 2;
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        //сортировка быстрая
        static int PartitionDigit(int[] array, int start, int end)
        {
            int marker = start;
            for (int i = start; i < end; i++)
            {
                if (array[i] < array[end])
                {
                    (array[marker], array[i]) = (array[i], array[marker]);
                    marker += 1;
                }
            }

            (array[marker], array[end]) = (array[end], array[marker]);
            return marker;
        }

        static int PartitionDate(DateTime[] array, int start, int end)
        {
            int marker = start;
            for (int i = start; i < end; i++)
            {
                if (array[i] < array[end])
                {
                    (array[marker], array[i]) = (array[i], array[marker]);
                    marker += 1;
                }
            }

            (array[marker], array[end]) = (array[end], array[marker]);
            return marker;
        }

        static void QuickSortDigit(int[] array, int start, int end)
        {

            if (start >= end)
                return;

            int pivot = PartitionDigit(array, start, end);
            QuickSortDigit(array, start, pivot - 1);
            QuickSortDigit(array, pivot + 1, end);
        }

        public static void QuickSortString(string[] arr, int left, int right)
        {
            int i = left, j = right;
            string pivot = arr[(left + right) / 2];
            while (i <= j)
            {
                while (arr[i].CompareTo(pivot) < 0)
                {
                    i++;
                }

                while (arr[j].CompareTo(pivot) > 0)
                {
                    j--;
                }

                if (i <= j)
                {
                    string temp = arr[i];
                    arr[i] = arr[j];
                    arr[j] = temp;
                    i++;
                    j--;
                }
            }

            if (left < j)
            {
                QuickSortString(arr, left, j);
            }

            if (i < right)
            {
                QuickSortString(arr, i, right);
            }
        }

        static void QuickSortDate(DateTime[] array, int start, int end)
        {

            if (start >= end)
                return;

            int pivot = PartitionDate(array, start, end);
            QuickSortDate(array, start, pivot - 1);
            QuickSortDate(array, pivot + 1, end);
        }

        //сортирвка слиянием
        static void MergeDigit(int[] a, int l, int m, int r)
        {
            int i, j, k;

            int n1 = m - l + 1;
            int n2 = r - m;

            int[] left = new int[n1 + 1];
            int[] right = new int[n2 + 1];

            for (i = 0; i < n1; i++)
            {
                left[i] = a[l + i];
            }

            for (j = 1; j <= n2; j++)
            {
                right[j - 1] = a[m + j];
            }

            left[n1] = int.MaxValue;
            right[n2] = int.MaxValue;

            i = 0;
            j = 0;

            for (k = l; k <= r; k++)
            {
                if (left[i] < right[j])
                {
                    a[k] = left[i];
                    i = i + 1;
                }
                else
                {
                    a[k] = right[j];
                    j = j + 1;
                }
            }
        }

        static void MergeDate(DateTime[] a, int l, int m, int r)
        {
            int i, j, k;

            int n1 = m - l + 1;
            int n2 = r - m;

            DateTime[] left = new DateTime[n1 + 1];
            DateTime[] right = new DateTime[n2 + 1];

            for (i = 0; i < n1; i++)
            {
                left[i] = a[l + i];
            }

            for (j = 1; j <= n2; j++)
            {
                right[j - 1] = a[m + j];
            }

            left[n1] = DateTime.MaxValue;
            right[n2] = DateTime.MaxValue;

            i = 0;
            j = 0;

            for (k = l; k <= r; k++)
            {
                if (left[i] < right[j])
                {
                    a[k] = left[i];
                    i = i + 1;
                }
                else
                {
                    a[k] = right[j];
                    j = j + 1;
                }
            }
        }

        static void MergeSortDigit(int[] a, int l, int r)
        {
            int q;

            if (l < r)
            {
                q = (l + r) / 2;
                MergeSortDigit(a, l, q);
                MergeSortDigit(a, q + 1, r);
                MergeDigit(a, l, q, r);
            }
        }

        public static void MergeSortString(string[] arr)
        {
            if (arr.Length < 2) return; // Если массив пустой или содержит только один элемент, то он уже отсортирован

            // Разделяем массив на две части
            int middle = arr.Length / 2;
            string[] left = new string[middle];
            string[] right = new string[arr.Length - middle];
            Array.Copy(arr, 0, left, 0, middle);
            Array.Copy(arr, middle, right, 0, arr.Length - middle);

            // Рекурсивно сортируем каждую из частей
            MergeSortString(left);
            MergeSortString(right);

            // Объединяем отсортированные части в один массив
            int i = 0, j = 0, k = 0;
            while (i < left.Length && j < right.Length)
            {
                if (string.Compare(left[i], right[j]) < 0)
                    arr[k++] = left[i++];
                else
                    arr[k++] = right[j++];
            }

            while (i < left.Length)
                arr[k++] = left[i++];

            while (j < right.Length)
                arr[k++] = right[j++];
        }

        static void MergeSortDate(DateTime[] a, int l, int r)
        {
            int q;

            if (l < r)
            {
                q = (l + r) / 2;
                MergeSortDate(a, l, q);
                MergeSortDate(a, q + 1, r);
                MergeDate(a, l, q, r);
            }
        }

        //сортировка кучей
        static int Add2HeapDigit(int[] arr, int i, int N)
        {
            int imax;
            int buf;
            if ((2 * i + 2) < N)
            {
                if (arr[2 * i + 1] < arr[2 * i + 2]) imax = 2 * i + 2;
                else imax = 2 * i + 1;
            }
            else imax = 2 * i + 1;

            if (imax >= N) return i;
            if (arr[i] < arr[imax])
            {
                buf = arr[i];
                arr[i] = arr[imax];
                arr[imax] = buf;
                if (imax < N / 2) i = imax;
            }

            return i;
        }

        static int Add2HeapDate(DateTime[] arr, int i, int N)
        {
            int imax;
            DateTime buf;
            if ((2 * i + 2) < N)
            {
                if (arr[2 * i + 1] < arr[2 * i + 2]) imax = 2 * i + 2;
                else imax = 2 * i + 1;
            }
            else imax = 2 * i + 1;

            if (imax >= N) return i;
            if (arr[i] < arr[imax])
            {
                buf = arr[i];
                arr[i] = arr[imax];
                arr[imax] = buf;
                if (imax < N / 2) i = imax;
            }

            return i;
        }

        static double HeapSortDigit(int[] arr, int len)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            //step 1: building the pyramid
            for (int i = len / 2 - 1; i >= 0; --i)
            {
                long prev_i = i;
                i = Add2HeapDigit(arr, i, len);
                if (prev_i != i) ++i;
            }

            //step 2: sorting
            int buf;
            for (int k = len - 1; k > 0; --k)
            {
                buf = arr[0];
                arr[0] = arr[k];
                arr[k] = buf;
                int i = 0, prev_i = -1;
                while (i != prev_i)
                {
                    prev_i = i;
                    i = Add2HeapDigit(arr, i, k);
                }
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        static void Heapify(string[] arr, int n, int i)
        {
            int largest = i; // инициализируем наибольший элемент как корень
            int l = 2 * i + 1; // левый дочерний элемент
            int r = 2 * i + 2; // правый дочерний элемент

            // если левый дочерний элемент больше корня
            if (l < n && String.Compare(arr[l], arr[largest]) > 0)
                largest = l;

            // если правый дочерний элемент больше, чем наибольший элемент на данный момент
            if (r < n && String.Compare(arr[r], arr[largest]) > 0)
                largest = r;

            // если наибольший элемент не корень
            if (largest != i)
            {
                // меняем корень и наибольший элемент
                string swap = arr[i];
                arr[i] = arr[largest];
                arr[largest] = swap;

                // рекурсивно вызываем Heapify для поддерева
                Heapify(arr, n, largest);
            }
        }

        public static double HeapSortString(string[] arr)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            int n = arr.Length;

            // построение кучи (перегруппировка массива)
            for (int i = n / 2 - 1; i >= 0; i--)
                Heapify(arr, n, i);

            // извлечение элементов из кучи в упорядоченном порядке
            for (int i = n - 1; i > 0; i--)
            {
                // перемещаем текущий корень в конец массива
                string temp = arr[0];
                arr[0] = arr[i];
                arr[i] = temp;

                // вызываем процедуру Heapify на уменьшенной куче
                Heapify(arr, i, 0);
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }

        static double HeapSortDate(DateTime[] arr, int len)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            //step 1: building the pyramid
            for (int i = len / 2 - 1; i >= 0; --i)
            {
                long prev_i = i;
                i = Add2HeapDate(arr, i, len);
                if (prev_i != i) ++i;
            }

            //step 2: sorting
            DateTime buf;
            for (int k = len - 1; k > 0; --k)
            {
                buf = arr[0];
                arr[0] = arr[k];
                arr[k] = buf;
                int i = 0, prev_i = -1;
                while (i != prev_i)
                {
                    prev_i = i;
                    i = Add2HeapDate(arr, i, k);
                }
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }


        //поразрядная сортировка
        public static double RadixSortDigit(int[] arr)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            int i, j;
            var tmp = new int[arr.Length];
            for (int shift = sizeof(int) * 8 - 1; shift > -1; --shift)
            {
                j = 0;
                for (i = 0; i < arr.Length; ++i)
                {
                    var move = (arr[i] << shift) >= 0;
                    if (shift == 0 ? !move : move)
                        arr[i - j] = arr[i];
                    else
                        tmp[j++] = arr[i];
                }

                Array.Copy(tmp, 0, arr, arr.Length - j, j);
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }
        public static double RadixSortString(string[] arr)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            // определяем максимальную длину строки в массиве
            int maxLength = 0;
            foreach (string s in arr)
            {
                if (s.Length > maxLength)
                    maxLength = s.Length;
            }

            // создаем 256 корзин, каждая из которых будет содержать строки определенной длины
            List<string>[] buckets = new List<string>[256];
            for (int i = 0; i < 256; i++)
                buckets[i] = new List<string>();

            // итерируемся по символам каждой строки, начиная с конца
            for (int digit = maxLength - 1; digit >= 0; digit--)
            {
                // помещаем каждую строку в соответствующую корзину в зависимости от значения текущего символа
                foreach (string s in arr)
                {
                    if (s.Length >= digit + 1)
                        buckets[(int)s[digit]].Add(s);
                    else
                        buckets[0].Add(s);
                }

                // переносим строки из корзин обратно в исходный массив
                int index = 0;
                for (int i = 0; i < 256; i++)
                {
                    foreach (string s in buckets[i])
                    {
                        arr[index] = s;
                        index++;
                    }

                    buckets[i].Clear();
                }
            }

            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }
        public static double RadixSortDate(DateTime[] arr)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            int n = arr.Length;
            DateTime[] output = new DateTime[n];
            int[] count = new int[256];

            for (int shift = 0; shift < 8 * sizeof(long); shift += 8)
            {
                for (int i = 0; i < 256; ++i)
                {
                    count[i] = 0;
                }

                for (int i = 0; i < n; ++i)
                {
                    long value = arr[i].Ticks >> shift;
                    int index = (int)(value & 0xff);
                    count[index]++;
                }

                for (int i = 1; i < 256; ++i)
                {
                    count[i] += count[i - 1];
                }

                for (int i = n - 1; i >= 0; --i)
                {
                    long value = arr[i].Ticks >> shift;
                    int index = (int)(value & 0xff);
                    output[count[index] - 1] = arr[i];
                    count[index]--;
                }

                for (int i = 0; i < n; ++i)
                {
                    arr[i] = output[i];
                }
            }
            
            stopwatch.Stop();
            return stopwatch.Elapsed.TotalMilliseconds;
        }
    }
}