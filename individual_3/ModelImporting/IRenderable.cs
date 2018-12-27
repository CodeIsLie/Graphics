using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ModelImporting
{
    public interface IRenderable
    {
        void Draw(uint shader, Transform transform, Camera camera, Projection projection, Lighting lighting);
    }
}
