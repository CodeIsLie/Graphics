using GlmNet;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Tao.OpenGl;

namespace ModelImporting
{
    public class Transform
    {
        public mat4 ModelMatrix { get; set; }

        public void Setup(uint shader)
        {
            int modelLoc = Gl.glGetUniformLocation(shader, "model");
            Gl.glUniformMatrix4fv(modelLoc, 1, Gl.GL_FALSE, ModelMatrix.to_array());
        }
    }
}
