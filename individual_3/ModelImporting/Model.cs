using Assimp;
using Assimp.Unmanaged;
using GlmNet;
using SquareSharpGLScene;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ModelImporting
{
    public class Model : IRenderable
    {
        private List<ModelMesh> meshes = new List<ModelMesh>();
        private string directory = "";

        public Model(string path, string directory)
        {
            this.directory = directory;
            Load(path);
        }

        public void Draw(uint shader, Transform transform, Camera camera, Projection projection, Lighting lighting)
        {
            foreach (var mesh in meshes)
            {
                mesh.Draw(shader, transform, camera, projection, lighting);
            }
        }

        public void SetCustomTexture(uint id)
        {
            foreach (var mesh in meshes)
            {
                mesh.CustomTexture = id;
            }
        }

        private void Load(string path)
        {
            AssimpContext importer = new AssimpContext();
            Scene scene = importer.ImportFile(path, PostProcessSteps.Triangulate);

            //directory = path.(0, path.find_last_of('/'));

            ProcessNode(scene.RootNode, scene);
        }

        private void ProcessNode(Node node, Scene scene)
        {
            for (var i = 0; i < node.MeshCount; ++i)
            {
                Mesh mesh = scene.Meshes[node.MeshIndices[i]];
                meshes.Add(ProcessMesh(mesh, scene));
            }

            for (var i = 0; i < node.ChildCount; ++i)
            {
                ProcessNode(node.Children[i], scene);
            }
        }

        private ModelMesh ProcessMesh(Mesh mesh, Scene scene)
        {
            List<ModelMesh.Vertex> vertices = new List<ModelMesh.Vertex>();
            List<uint> indices = new List<uint>();
            List<ModelMesh.Texture> textures = new List<ModelMesh.Texture>();

            for (var i = 0; i < mesh.VertexCount; ++i)
            {
                var vertex = new ModelMesh.Vertex();

                vec3 vector = new vec3();
                vector.x = mesh.Vertices[i].X;
                vector.y = mesh.Vertices[i].Y;
                vector.z = mesh.Vertices[i].Z;
                vertex.Position = vector;

                vector.x = mesh.Normals[i].X;
                vector.y = mesh.Normals[i].Y;
                vector.z = mesh.Normals[i].Z;
                vertex.Normal = vector;

                if (mesh.HasTextureCoords(0))
                {
                    vec2 vec = new vec2();
                    vec.x = mesh.TextureCoordinateChannels[0][i].X;
                    vec.y = mesh.TextureCoordinateChannels[0][i].Y;
                    vertex.TexCoords = vec;
                }
                else
                {
                    vertex.TexCoords = new vec2(0.0f, 0.0f);
                }

                vertices.Add(vertex);
            }

            for (var i = 0; i < mesh.FaceCount; ++i)
            {
                Face face = mesh.Faces[i];
                for (var j = 0; j < face.IndexCount; ++j)
                {
                    indices.Add((uint)face.Indices[j]);
                } 
            }

            if (mesh.MaterialIndex >= 0)
            {
                Material material = scene.Materials[mesh.MaterialIndex];
                List<ModelMesh.Texture> diffuseMaps = LoadMaterialTextures(material,
                                                    TextureType.Diffuse, ModelMesh.Texture.TextureType.Diffuse);

                textures.AddRange(diffuseMaps);
                List<ModelMesh.Texture> specularMaps = LoadMaterialTextures(material,
                                                    TextureType.Specular, ModelMesh.Texture.TextureType.Specular);
                textures.AddRange(specularMaps);
            }

            return new ModelMesh(vertices, indices, textures);
        }

        private List<ModelMesh.Texture> LoadMaterialTextures(Material mat, TextureType type, ModelMesh.Texture.TextureType modelType)
        {
            List<ModelMesh.Texture> textures = new List<ModelMesh.Texture>();
            for (var i = 0; i < mat.GetMaterialTextureCount(type); ++i)
            {
                TextureSlot slot = new TextureSlot();
                mat.GetMaterialTexture(type, i, out slot);
                var fullPath = @"..\..\" + directory + @"\" + slot.FilePath;
                ModelMesh.Texture texture = new ModelMesh.Texture()
                {
                    Id = (uint)TextureUtil.LoadTexture(fullPath),
                    Type = modelType
                };

                textures.Add(texture);
            }
            return textures;
        }
    }
}
