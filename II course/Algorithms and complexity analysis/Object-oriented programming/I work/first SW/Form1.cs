using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Security;
using System.Text.RegularExpressions;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml.Schema;


/*
    1. Ввод текста через текстовое поле или файл в форму
    2. Статистика по тексту:
        1)Количество слов
        2)Количество уникальных слов
        3)10 самых длинных слов в тексте (по убыванию)
        4)10 самых часто встречаемых слов 
        5)Процентаж каждого символа (пр. 'a'-2%, 'b'-0,5% ...)
*/

namespace first_SW
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            textBox1.ScrollBars = ScrollBars.Vertical;
        }
        class Analysis
        {
            public Analysis(TextBox textBox1) { }
            private string[] txtbox2stringarr(TextBox textBox1)
            {
                string text = textBox1.Text;
                char[] separators = new char[] { ' ', '-', '.', ',', '"', '%', '\t', ':', '(', ')', '\n','!', '?', '*', '/', '+','^', '\v' };
                string[] textMass = text.Split(separators, StringSplitOptions.RemoveEmptyEntries);
                return textMass;
            }
            private static string RemovePunctuations(TextBox textBox1)
            {
                string text = textBox1.Text;
                return Regex.Replace(text, "[!\"#$%&'()*+,-./:;<=>?@\\[\\]^_`{|}~ ]", string.Empty);
            }
            public string WordNumbers(TextBox textBox1)
            { //1
            int spaces = txtbox2stringarr(textBox1).Length;
            string temp = "В данном тексте " + spaces + " слов \n";
            return temp;
            }
            public string UniqeuWords(TextBox textBox1)
            {
                int UniqueElements = 0;
                bool found = false;
                for (int i = 0; i < txtbox2stringarr(textBox1).Length; i++)
                {
                    found = false;
                    for (int j = 0; j < txtbox2stringarr(textBox1).Length; j++)
                    {
                        if (i != j && txtbox2stringarr(textBox1)[i] == txtbox2stringarr(textBox1)[j])
                        {
                            found = true;
                            break;
                        }
                    }
                    if (!found) UniqueElements++;
                }
                string temp2 = "Уникальных слов в данном тексте: " + UniqueElements + "\n";
                return temp2;
            }
            public string TopLongestWords(TextBox textBox1)
            {
                List<string> wordlist = new List<string>();
                for (int i = 0; i < txtbox2stringarr(textBox1).Length; i++)
                {
                    wordlist.Add(txtbox2stringarr(textBox1)[i]);
                }
                int left = 0;
                int right = wordlist.Count - 1;
                int count = 0;
                while (left <= right)
                {
                    for (int i = left; i < right; i++)
                    {
                        count++;
                        if (wordlist[i].Length < wordlist[i + 1].Length)
                            Swap(wordlist, i, i + 1);
                    }

                    right--;

                    for (int i = right; i > left; i--)
                    {
                        count++;
                        if (wordlist[i - 1].Length < wordlist[i].Length)
                            Swap(wordlist, i - 1, i);
                    }

                    left++;
                }
                int counter = wordlist.Count;
                string temp3 = "10 самых длинных слов в вашем тексте: \n";
                if (wordlist.Count < 10)
                {
                    for (int i = 0; i < counter; i++)
                    {
                        temp3 += (i+1) + ". " + wordlist.First() + "\n ";
                        wordlist.Remove(wordlist.First());
                    }
                }
                else{
                    for (int i = 0; i < 10; i++) 
                    {
                        temp3 += (i+1) + ". " + wordlist.First() + "\n ";
                        wordlist.Remove(wordlist.First());
                    }
                }

                temp3 += "\n";
                return temp3;
            }
            public string TopMostPopularWords(TextBox textBox1)
            {
                string temp4 = "10 самых часто встречаемых слов: \n";
                Dictionary<string, int> maxwords = new Dictionary<string, int>();
                for (int j = 0; j < txtbox2stringarr(textBox1).Length; j++)
                {
                    if (maxwords.ContainsKey(txtbox2stringarr(textBox1)[j])) maxwords[txtbox2stringarr(textBox1)[j]]++;
                    else maxwords.Add(txtbox2stringarr(textBox1)[j], 1);
                }

                maxwords = maxwords.OrderByDescending(x => x.Value).ToDictionary(x => x.Key, x => x.Value);
                int m = 0;
                foreach (var word in maxwords)
                {
                    if (m > 9) break;
                    temp4 += m+1+". " + word.Key + " - " + word.Value + "\n";
                    m++;
                }

                return temp4;
            }
            public string PercentageInText(TextBox textBox1)
            {
                Dictionary<char, double> symbols = new Dictionary<char, double>();
                string stralp = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z А Б В Г Д Е Ё Ж З И К Л М Н О П Р С Т У Ф Х Ц Ч Ь Ы Ъ Э Ю Я а б в г д е ё ж з и к л м н о п р с т у ф х ц ч ь ы ъ э ю я";
                char[] chrlt = stralp.ToCharArray();
                for (int j = 0; j < chrlt.Length; j++)
                {
                    if (symbols.ContainsKey(chrlt[j])) symbols[chrlt[j]]++;
                    else symbols.Add(chrlt[j], 0);
                }

                string text1 = RemovePunctuations(textBox1);
                text1 = text1.Replace(" ","");
                char[] letters = text1.ToCharArray();
                for (int j = 0; j < letters.Length; j++)
                {
                    if (symbols.ContainsKey(letters[j]) && letters[j]!=' ') symbols[letters[j]]++;
                }
                
                var keyToRemove = ' ';
                symbols.Remove(keyToRemove);

                double sum = letters.Length ;
                // осталось сделать оформление
                string temp5 = "";
                int enter = 0;
                int ar = 0;

                
                foreach (var lett in symbols)
                {
                    if (lett.Key == ' ')
                    {
                        temp5 += ' ';
                    }
                    else
                    {
                        temp5 += (lett.Key + "-" + (Math.Round((lett.Value / sum) * 100)) + "% \t");
                        if (lett.Key == 'M' || lett.Key == 'Z' || lett.Key == 'm' || lett.Key == 'z' || lett.Key == 'П' || lett.Key == 'Я' || lett.Key == 'п' || lett.Key == 'я')
                        { 
                            temp5 += '\n';
                        }
                        if (lett.Key == 'Z' || lett.Key == 'z' || lett.Key == 'Я' || lett.Key == 'я')
                        { 
                            temp5 += '\n';
                        }
                    }
                }
                
                return temp5;
            }
            static void Swap(List<string> list, int i, int j)
            {
                string x = list[i];
                list[i] = list[j];
                list[j] = x;
            }
        };
        private void button1_Click(object sender, EventArgs e)
        {
            if (textBox1.Text.Length == 0)
            {
                MessageBox.Show("Для начала работы необходимо ввести текст!");
            }
            else{
                Analysis an = new Analysis(textBox1);
                label1.Text = an.WordNumbers(textBox1);
                label2.Text = an.UniqeuWords(textBox1);
                label3.Text = an.TopLongestWords(textBox1);
                label4.Text = an.TopMostPopularWords(textBox1);
                label5.Text = an.PercentageInText(textBox1);
            }
            GC.Collect();
        }
        private void button2_Click(object sender, EventArgs e)
        {
            OpenFileDialogForm f = new OpenFileDialogForm(100);
            f.ShowDialog();
            this.textBox1.Text = f.textBox1.Text;
        }
        private void button3_Click(object sender, EventArgs e)
        {
            Close();
        }
    }
}
