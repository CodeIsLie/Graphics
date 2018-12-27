using GlmNet;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Tao.OpenGl;

namespace ModelImporting
{
    public class ModelMesh
    {
        public class Vertex
        {
            public vec3 Position { get; set; }
            public vec3 Normal { get; set; }
            public vec2 TexCoords { get; set; }
        }

        public class Texture
        {
            public enum TextureType { Diffuse, Specular }
            public uint Id { get; set; }
            public TextureType Type { get; set; }
        }

        private uint vbo, ebo;

        public uint CustomTexture { get; set; }
        public List<Vertex> Vertices { get; } = new List<Vertex>();
        public List<uint> Indices { get; } = new List<uint>();
        public List<Texture> Textures { get; } = new List<Texture>();

        public ModelMesh(List<Vertex> vertices, List<uint> indices, List<Texture> textures)
        {
            Vertices = vertices;
            Indices = indices;
            Textures = textures;
            Setup();
        }

        public void Draw(uint shader, Transform transform, Camera camera, Projection projection, Lighting lighting)
        {
            uint diffuseNumber = 1;
            uint specularNumber = 1;
            if (Textures.Count == 0)
            {
                Gl.glActiveTexture(Gl.GL_TEXTURE0);
                int textureLoc = Gl.glGetUniformLocation(shader, "material.textureDiffuse1");
                Gl.glUniform1i(textureLoc, 0);
                Gl.glBindTexture(Gl.GL_TEXTURE_2D, CustomTexture);
            }

            for (int i = 0; i < Textures.Count; ++i)
            {
                Gl.glActiveTexture(Gl.GL_TEXTURE0 + i);
                string name = "texture" + Textures[i].Type.ToString();
                if (Textures[i].Type == Texture.TextureType.Diffuse)
                {
                    name += diffuseNumber.ToString();
                    ++diffuseNumber;
                }
                else
                {
                    name += specularNumber.ToString();
                    ++specularNumber;
                }

                int textureLoc = Gl.glGetUniformLocation(shader, "material." + name.ToString());
                Gl.glUniform1i(textureLoc, i);
                Gl.glBindTexture(Gl.GL_TEXTURE_2D, Textures[i].Id);
            }

            Gl.glUseProgram(shader);
            Gl.glActiveTexture(Gl.GL_TEXTURE0);

            Gl.glBindBuffer(Gl.GL_ELEMENT_ARRAY_BUFFER, ebo);
            Gl.glBufferData(Gl.GL_ELEMENT_ARRAY_BUFFER, (IntPtr)(Indices.Count * sizeof(float)), Indices.ToArray(), Gl.GL_STATIC_DRAW);
            
            Gl.glBindBuffer(Gl.GL_ARRAY_BUFFER, vbo);
            var buf = GetVertices();
            Gl.glBufferData(Gl.GL_ARRAY_BUFFER, (IntPtr)(buf.Length * sizeof(float)), GetVertices(), Gl.GL_STATIC_DRAW);
            
            Gl.glVertexAttribPointer(0, 3, Gl.GL_FLOAT, Gl.GL_FALSE, 8 * sizeof(float), new IntPtr(0));
            Gl.glEnableVertexAttribArray(0);

            Gl.glVertexAttribPointer(1, 2, Gl.GL_FLOAT, Gl.GL_FALSE, 8 * sizeof(float), new IntPtr(3 * sizeof(float)));
            Gl.glEnableVertexAttribArray(1);

            Gl.glVertexAttribPointer(2, 3, Gl.GL_FLOAT, Gl.GL_FALSE, 8 * sizeof(float), new IntPtr(5 * sizeof(float)));
            Gl.glEnableVertexAttribArray(2);

            int shininessLoc = Gl.glGetUniformLocation(shader, "material.shininess");
            Gl.glUniform1f(shininessLoc, 32.0f);

            lighting.Setup(shader);
            transform.Setup(shader);
            camera.Setup(shader);
            projection.Setup(shader);

            Gl.glBindBuffer(Gl.GL_ELEMENT_ARRAY_BUFFER, ebo);
            Gl.glDrawElements(Gl.GL_TRIANGLES, Indices.Count, Gl.GL_UNSIGNED_INT, new IntPtr(0));
        }

        private void SetupLighting(uint shader, Camera camera)
        {
            int ambientColorLoc = Gl.glGetUniformLocation(shader, "light.ambient");
            Gl.glUniform3f(ambientColorLoc, 0.5f, 0.5f, 0.5f);

            int diffuseColorLoc = Gl.glGetUniformLocation(shader, "light.diffuse");
            Gl.glUniform3f(diffuseColorLoc, 0.5f, 0.5f, 0.5f);

            int specularColorLoc = Gl.glGetUniformLocation(shader, "light.specular");
            Gl.glUniform3f(specularColorLoc, 1.0f, 1.0f, 1.0f);

            int lightPosLoc = Gl.glGetUniformLocation(shader, "light.position");
            Gl.glUniform3f(lightPosLoc, 0, 0, 0);

            int viewPosLoc = Gl.glGetUniformLocation(shader, "viewPos");
            Gl.glUniform3f(viewPosLoc, camera.Position.x, camera.Position.y, camera.Position.z);
        }

        private float[] GetVertices()
        {
            float[] res = new float[Vertices.Count * 8];
            int i = 0;
            foreach (var v in Vertices)
            {
                res[i++] = v.Position.x;
                res[i++] = v.Position.y;
                res[i++] = v.Position.z;

                res[i++] = v.TexCoords.x;
                res[i++] = v.TexCoords.y;

                res[i++] = v.Normal.x;
                res[i++] = v.Normal.y;
                res[i++] = v.Normal.z;
            }

            return res;
        }

        private void Setup()
        {
            Gl.glGenBuffers(1, out vbo);
            Gl.glGenBuffers(1, out ebo);

            // 1. Настраиваем буфер индексов
            Gl.glBindBuffer(Gl.GL_ELEMENT_ARRAY_BUFFER, ebo);
            Gl.glBufferData(Gl.GL_ELEMENT_ARRAY_BUFFER, (IntPtr)(Indices.Count * sizeof(float)), Indices.ToArray(), Gl.GL_STATIC_DRAW);

            // 2. Копируем наш массив вершин в буфер для OpenGL
            Gl.glBindBuffer(Gl.GL_ARRAY_BUFFER, vbo);
            var buf = GetVertices();
            Gl.glBufferData(Gl.GL_ARRAY_BUFFER, (IntPtr)(buf.Length * sizeof(float)), GetVertices(), Gl.GL_STATIC_DRAW);

            // 3. Устанавливаем указатели на вершинные атрибуты 
            Gl.glVertexAttribPointer(0, 3, Gl.GL_FLOAT, Gl.GL_FALSE, 8 * sizeof(float), new IntPtr(0));
            Gl.glEnableVertexAttribArray(0);

            Gl.glVertexAttribPointer(1, 2, Gl.GL_FLOAT, Gl.GL_FALSE, 8 * sizeof(float), new IntPtr(3 * sizeof(float)));
            Gl.glEnableVertexAttribArray(1);

            Gl.glVertexAttribPointer(2, 3, Gl.GL_FLOAT, Gl.GL_FALSE, 8 * sizeof(float), new IntPtr(5 * sizeof(float)));
            Gl.glEnableVertexAttribArray(2);
        }
    }
}
