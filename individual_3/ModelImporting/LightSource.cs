using GlmNet;
using SimpleShaders;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Tao.Glfw;
using Tao.OpenGl;

namespace ModelImporting
{
    public class LightSource : IRenderable
    {
        private float[] vertices;
        private uint vbo;

        public vec3 Position { get; set; }

        public LightSource()
        {
            vertices = new float[]
            {
                -0.5f, -0.5f, -0.5f,
                 0.5f, -0.5f, -0.5f,
                 0.5f,  0.5f, -0.5f,
                 0.5f,  0.5f, -0.5f,
                -0.5f,  0.5f, -0.5f,
                -0.5f, -0.5f, -0.5f,

                -0.5f, -0.5f,  0.5f,
                 0.5f, -0.5f,  0.5f,
                 0.5f,  0.5f,  0.5f,
                 0.5f,  0.5f,  0.5f,
                -0.5f,  0.5f,  0.5f,
                -0.5f, -0.5f,  0.5f,

                -0.5f,  0.5f,  0.5f,
                -0.5f,  0.5f, -0.5f,
                -0.5f, -0.5f, -0.5f,
                -0.5f, -0.5f, -0.5f,
                -0.5f, -0.5f,  0.5f,
                -0.5f,  0.5f,  0.5f,

                 0.5f,  0.5f,  0.5f,
                 0.5f,  0.5f, -0.5f,
                 0.5f, -0.5f, -0.5f,
                 0.5f, -0.5f, -0.5f,
                 0.5f, -0.5f,  0.5f,
                 0.5f,  0.5f,  0.5f,

                -0.5f, -0.5f, -0.5f,
                 0.5f, -0.5f, -0.5f,
                 0.5f, -0.5f,  0.5f,
                 0.5f, -0.5f,  0.5f,
                -0.5f, -0.5f,  0.5f,
                -0.5f, -0.5f, -0.5f,

                -0.5f,  0.5f, -0.5f,
                 0.5f,  0.5f, -0.5f,
                 0.5f,  0.5f,  0.5f,
                 0.5f,  0.5f,  0.5f,
                -0.5f,  0.5f,  0.5f,
                -0.5f,  0.5f, -0.5f
            };

            Gl.glGenBuffers(1, out vbo);
            
            Gl.glBindBuffer(Gl.GL_ARRAY_BUFFER, vbo);
            Gl.glBufferData(Gl.GL_ARRAY_BUFFER, (IntPtr)(vertices.Length * sizeof(float)), vertices, Gl.GL_STATIC_DRAW);
            
            Gl.glVertexAttribPointer(0, 3, Gl.GL_FLOAT, Gl.GL_FALSE, 3 * sizeof(float), new IntPtr(0));
            Gl.glEnableVertexAttribArray(0);
        }

        public void Draw(uint shader, Transform transform, Camera camera, Projection projection, Lighting lighting)
        {
            Gl.glBindBuffer(Gl.GL_ARRAY_BUFFER, vbo);
            Gl.glBufferData(Gl.GL_ARRAY_BUFFER, (IntPtr)(vertices.Length * sizeof(float)), vertices, Gl.GL_STATIC_DRAW);
            
            Gl.glVertexAttribPointer(0, 3, Gl.GL_FLOAT, Gl.GL_FALSE, 3 * sizeof(float), new IntPtr(0));
            Gl.glEnableVertexAttribArray(0);
            
            Gl.glUseProgram(shader);
            
            transform.Setup(shader);
            camera.Setup(shader);
            projection.Setup(shader);

            Gl.glDrawArrays(Gl.GL_TRIANGLES, 0, vertices.Length / 3);
        }
    }
}
