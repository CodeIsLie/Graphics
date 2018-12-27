using GlmNet;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Tao.OpenGl;

namespace ModelImporting
{
    public class Projection
    {
        public Projection()
        {
        }

        public void Setup(uint shader)
        {
            mat4 projMatrix = glm.perspective(glm.radians(45.0f), MainWindow.SceneWidth / (float)MainWindow.SceneHeight, 0.1f, 100.0f);
            int projLoc = Gl.glGetUniformLocation(shader, "projection");
            Gl.glUniformMatrix4fv(projLoc, 1, Gl.GL_FALSE, projMatrix.to_array());
        }
    }
}
