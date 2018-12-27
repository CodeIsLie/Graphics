using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ModelImporting
{
    public static class ModelLoader
    {
        public static void Load(string path, out float[] inVertices, out uint[] inIndices)
        {
            var file = System.IO.File.ReadAllLines(path);
            var vertices = file
                .Where(str => str.StartsWith("v "))
                .Select(str =>
                        str.ToString().Trim().Split().Skip(1)
                        .Select(x => float.Parse(x)));

            var indices = file
                .Where(str => str.StartsWith("f "))
                .Select(str =>
                       str.ToString().Trim().Split().Skip(1)
                       .Select(x => uint.Parse(x.Split('/').First())).ToArray())
                .ToArray();

            var texCoords = file
                .Where(str => str.StartsWith("vt "))
                .Select(str =>
                        str.ToString().Trim().Split().Skip(2).Take(2)
                        .Select(x => float.Parse(x)).ToArray())
                .ToArray();

            var normals = file
                .Where(str => str.StartsWith("vn "))
                .Select(str =>
                        str.ToString().Trim().Split().Skip(2).Take(3)
                        .Select(x => float.Parse(x)).ToArray())
                .ToArray();

            var normalIndices = file
               .Where(str => str.StartsWith("f "))
               .Select(str =>
                      str.ToString().Trim().Split().Skip(1)
                      .Select(x => uint.Parse(x.Split('/').Skip(2).First())).ToArray())
               .ToArray();

            var texIndices = file
                .Where(str => str.StartsWith("f "))
                .Select(str =>
                       str.ToString().Trim().Split().Skip(1)
                       .Select(x => uint.Parse(x.Split('/').Skip(1).First())).ToArray())
                .ToArray();
            
            int i = 0;
            inIndices = new uint[indices.Count() * 3];
            foreach (var v in indices)
            {
                foreach (var e in v)
                {
                    inIndices[i++] = e - 1;
                }
            }

            i = 0;
            var texCoordsArray = new float[vertices.Count()][];
            for (int k = 0; k < vertices.Count(); ++k)
            {
                texCoordsArray[k] = new float[2];
            }
            
            for (var k = 0; k < texIndices.Length; ++k)
            {
                texCoordsArray[indices[k][0] - 1][0] = texCoords[texIndices[k][0] - 1][0];
                texCoordsArray[indices[k][0] - 1][1] = texCoords[texIndices[k][0] - 1][1];

                texCoordsArray[indices[k][1] - 1][0] = texCoords[texIndices[k][1] - 1][0];
                texCoordsArray[indices[k][1] - 1][1] = texCoords[texIndices[k][1] - 1][1];

                texCoordsArray[indices[k][2] - 1][0] = texCoords[texIndices[k][2] - 1][0];
                texCoordsArray[indices[k][2] - 1][1] = texCoords[texIndices[k][2] - 1][1];
            }

            i = 0;
            var normalArray = new float[vertices.Count()][];
            for (int k = 0; k < vertices.Count(); ++k)
            {
                normalArray[k] = new float[3];
            }

            for (var k = 0; k < normalIndices.Length; ++k)
            {
                normalArray[indices[k][0] - 1][0] = normals[normalIndices[k][0] - 1][0];
                normalArray[indices[k][0] - 1][1] = normals[normalIndices[k][0] - 1][1];
                normalArray[indices[k][0] - 1][2] = normals[normalIndices[k][0] - 1][2];

                normalArray[indices[k][1] - 1][0] = normals[normalIndices[k][1] - 1][0];
                normalArray[indices[k][1] - 1][1] = normals[normalIndices[k][1] - 1][1];
                normalArray[indices[k][1] - 1][2] = normals[normalIndices[k][1] - 1][2];

                normalArray[indices[k][2] - 1][0] = normals[normalIndices[k][2] - 1][0];
                normalArray[indices[k][2] - 1][1] = normals[normalIndices[k][2] - 1][1];
                normalArray[indices[k][2] - 1][2] = normals[normalIndices[k][2] - 1][2];
            }

            inVertices = new float[vertices.Count() * 8];
            i = 0;
            int vertInd = 0;
            foreach (var v in vertices)
            {
                foreach (var e in v)
                {
                    inVertices[i++] = e;
                }
                inVertices[i++] = texCoordsArray[vertInd][0];
                inVertices[i++] = texCoordsArray[vertInd][1];

                inVertices[i++] = normalArray[vertInd][0];
                inVertices[i++] = normalArray[vertInd][1];
                inVertices[i++] = normalArray[vertInd][2];

                ++vertInd;
            }
        }
    }
}
