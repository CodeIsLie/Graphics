using GlmNet;
using SimpleShaders;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Tao.OpenGl;

namespace ModelImporting
{
    public class Plane : IRenderable
    {
        private uint vbo;
        private float[] vertices;
        
        public uint DiffuseMap { get; set; }
        public uint SpecularMap { get; set; }

        public Plane(uint diffuseMap, uint specularMap)
        {
            DiffuseMap = diffuseMap;
            SpecularMap = specularMap;
            
            vertices = new float[32]
            {
                -1f, -1f, 0f, 0f, 0f, 0f, 0f, 1f,
                -1f, 1f, 0f, 0f, 1f, 0f, 0f, 1f,
                1f, 1f, 0f, 1f, 1f, 0f, 0f, 1f,
                1f, -1f, 0f, 1f, 0f, 0f, 0f, 1f
            };

            // VBO, EBO
            Gl.glGenBuffers(1, out vbo);

            // 2. Копируем наш массив вершин в буфер для OpenGL
            Gl.glBindBuffer(Gl.GL_ARRAY_BUFFER, vbo);
            Gl.glBufferData(Gl.GL_ARRAY_BUFFER, (IntPtr)(vertices.Length * sizeof(float)), vertices, Gl.GL_STATIC_DRAW);
            
            Gl.glVertexAttribPointer(0, 3, Gl.GL_FLOAT, Gl.GL_FALSE, 8 * sizeof(float), new IntPtr(0));
            Gl.glEnableVertexAttribArray(0);

            Gl.glVertexAttribPointer(1, 2, Gl.GL_FLOAT, Gl.GL_FALSE, 8 * sizeof(float), new IntPtr(3 * sizeof(float)));
            Gl.glEnableVertexAttribArray(1);

            Gl.glVertexAttribPointer(2, 3, Gl.GL_FLOAT, Gl.GL_FALSE, 8 * sizeof(float), new IntPtr(5 * sizeof(float)));
            Gl.glEnableVertexAttribArray(2);
        }

        public void Draw(uint shader, Transform transform, Camera camera, Projection projection, Lighting lighting)
        {
            Gl.glBindBuffer(Gl.GL_ARRAY_BUFFER, vbo);
            Gl.glBufferData(Gl.GL_ARRAY_BUFFER, (IntPtr)(vertices.Length * sizeof(float)), vertices, Gl.GL_STATIC_DRAW);
            
            Gl.glVertexAttribPointer(0, 3, Gl.GL_FLOAT, Gl.GL_FALSE, 8 * sizeof(float), new IntPtr(0));
            Gl.glEnableVertexAttribArray(0);

            Gl.glVertexAttribPointer(1, 2, Gl.GL_FLOAT, Gl.GL_FALSE, 8 * sizeof(float), new IntPtr(3 * sizeof(float)));
            Gl.glEnableVertexAttribArray(1);

            Gl.glVertexAttribPointer(2, 3, Gl.GL_FLOAT, Gl.GL_FALSE, 8 * sizeof(float), new IntPtr(5 * sizeof(float)));
            Gl.glEnableVertexAttribArray(2);
            
            Gl.glUseProgram(shader);

            Gl.glActiveTexture(Gl.GL_TEXTURE0);
            int textureDiffuseLoc = Gl.glGetUniformLocation(shader, "material.textureDiffuse1");
            Gl.glUniform1i(textureDiffuseLoc, 0);
            Gl.glBindTexture(Gl.GL_TEXTURE_2D, DiffuseMap);

            Gl.glActiveTexture(Gl.GL_TEXTURE1);
            int textureSpecularLoc = Gl.glGetUniformLocation(shader, "material.textureSpecular1");
            Gl.glUniform1i(textureSpecularLoc, 1);
            Gl.glBindTexture(Gl.GL_TEXTURE_2D, SpecularMap);

            Gl.glActiveTexture(Gl.GL_TEXTURE0);

            int shininessLoc = Gl.glGetUniformLocation(shader, "material.shininess");
            Gl.glUniform1f(shininessLoc, 32f);

            lighting.Setup(shader);
            transform.Setup(shader);
            camera.Setup(shader);
            projection.Setup(shader);

            Gl.glDrawArrays(Gl.GL_QUADS, 0, vertices.Length / 8);
        }
    }
}
