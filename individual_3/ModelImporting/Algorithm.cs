using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ModelImporting
{
    public static class Algorithm
    {
        public static float ToRadian(double degrees)
        {
            return (float)(degrees * Math.PI / 180);
        }
    }
}
