using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

/*
 Задаются: диапазон значений, функция, необходимо построить график
 с возможностью масштабирования – в максимальных и минимальных точках график 
 касается верхних и нижних границ графического окна. Обязательный тест – sin(x) и x^2. 
 Необходимо предусмотреть выбор функций из некоторого списка. В функцию построения графика 
 функцию передавать как параметр.
*/

namespace Graphics_1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            System.Object[] ItemObject = {"sin", "cos", "arctan", "x^2", "x^3" };
            listBox1.Items.AddRange(ItemObject);
            //listBox1.Font.Size = 14;
            listBox1.SelectedIndex = 0;
            textBox1.Text = "-1";
            textBox2.Text = "1";

            im = new Bitmap(pictureBox1.Width, pictureBox1.Height);
            pictureBox1.Image = im;
            g = Graphics.FromImage(pictureBox1.Image);
            g.Clear(Color.White);
        }

        private Graphics g;
        private Image im;
        double Apply(double x, Func<double, double> f) { return f(x); }

        void drawGraph(Func<double, double> f, double minX, double maxX)
        {
            List<double> Xvalues = new List<double>();
            List<double> Yvalues = new List<double>();

            double maxY = 0;
            double minY = 0;

            // int minX = -5;
            //int maxX = 5;
            double yDiff = 0;
            double koef = 1.0 / 5;

            int height = pictureBox1.Size.Height;
            int width = pictureBox1.Size.Width;
            //double k_draw = (maxX > maxY) ? pictureBox1.Size.Width / (1.1 * maxX) :
            //  pictureBox1.Size.Height / (1.1 * maxY);
            
            for (double i = minX; i < maxX; i+= 0.01)
            {
                double curF = f(i);
                maxY = (maxY > curF) ? maxY : curF;
                minY = (minY < curF) ? minY : curF;
                yDiff = maxY - minY;

                Xvalues.Add(i);
                Yvalues.Add(curF);
            }
            double xDiff = maxX - minX;            
            double k_draw_y = pictureBox1.Size.Height / (1.005 * yDiff);
            double k_draw_x = pictureBox1.Size.Width / (1.005 * xDiff);

            Pen pen = new Pen(Color.SlateBlue);           

            for (int i = 0; i < Xvalues.Count-1; ++i)
            {
                Point p1 = new Point(Convert.ToInt32(k_draw_x * (Xvalues[i] - minX)),
                                    -Convert.ToInt32(k_draw_y * (Yvalues[i] - minY)) + height-3);
                Point p2 = new Point(Convert.ToInt32(k_draw_x * (Xvalues[i+1] - minX)),
                                    -Convert.ToInt32(k_draw_y * (Yvalues[i+1] - minY)) + height-3);
                g.DrawLine(pen, p1, p2);
            }
            
            pen.Dispose();
            pictureBox1.Invalidate();
        }

        double xSquare(double x)
        {
            return x * x;
        }

        double xCube(double x)
        {
            return x * x * x;
        }

        public double Acot(double x)
        {
            return x == 0 ? 0 : Math.Atan(1 / x);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            // this.listBox1.t
            //drawGraph(Math.Sin);
            g.Clear(Color.White);
            Func<double, double> drawedFun = xCube;
            String item = listBox1.SelectedItem.ToString();
            switch (item)
            {
                case "sin":
                    drawedFun = Math.Sin;
                    break;
                case "cos":
                    drawedFun = Math.Cos;
                    break;
                case "arctan":
                    drawedFun = Math.Atan;
                    break;
                case "x^2":
                    drawedFun = xSquare;
                    break;
                case "x^3":
                    drawedFun = xCube;
                    break;

            }

            double minX=0, maxX=1;
            try
            {
                minX = Convert.ToDouble(textBox1.Text);
                maxX = Convert.ToDouble(textBox2.Text);
            } catch (Exception ex)
            {

            }
            if (minX < maxX)
            {
                drawGraph(drawedFun, minX, maxX);
            }
        }
    }
}
