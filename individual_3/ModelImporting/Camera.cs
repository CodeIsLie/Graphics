using GlmNet;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Tao.OpenGl;

namespace ModelImporting
{
    public class Camera
    {
        public float Sensitivity { get; set; } = 0.25f;
        public float Speed { get; set; } = 0.15f;
        public float Pitch { get; set; } = 0f;
        public float Yaw { get; set; } = -90f;

        public vec3 Position { get; set; } = new vec3(0, 0, 0);
        public vec3 Front { get; set; } = new vec3(0, 0, -1);
        public vec3 Up { get; set; } = new vec3(0, 1, 0);

        public Camera(vec3 position)
        {
            Position = position;
        }

        public void Setup(uint shader)
        {
            var viewMatrix = glm.lookAt(Position, Position + Front, Up);
            int viewLoc = Gl.glGetUniformLocation(shader, "view");
            Gl.glUniformMatrix4fv(viewLoc, 1, Gl.GL_FALSE, viewMatrix.to_array());

            int viewPosLoc = Gl.glGetUniformLocation(shader, "viewPos");
            Gl.glUniform3f(viewPosLoc, Position.x, Position.y, Position.z);
        }
    }
}
