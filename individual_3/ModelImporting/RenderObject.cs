using GlmNet;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ModelImporting
{
    public class RenderObject
    {
        public Transform ModelTransform { get; set; }

        public IRenderable Renderable { get; set; }

        public uint Shader { get; set; }

        public RenderObject(IRenderable renderable, Transform transform, uint shader)
        {
            Shader = shader;
            Renderable = renderable;
            ModelTransform = transform;
        }

        public void Render(Camera camera, Projection projection, Lighting lighting)
        {
            Renderable.Draw(Shader, ModelTransform, camera, projection, lighting);
        }
    }
}
