using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SimpleShaders
{
    public static class ShaderLoader
    {
        public static string Load(string path)
        {
            return System.IO.File.ReadAllText(path);
        }
    }
}
