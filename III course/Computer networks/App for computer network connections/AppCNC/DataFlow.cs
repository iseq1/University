using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AppCNC
{
    public class DataFlow
    {
        public string name;
        public double size;

        public DataFlow(double size)
        {
            this.size = size;
        }

        public double getSize()
        {
            return size;
        }

        public override string ToString()
        {
            return string.Format("\"{0}\" DataFlow: [{1}]", name, Math.Round(size, 2).ToString());
        }
    }
}
