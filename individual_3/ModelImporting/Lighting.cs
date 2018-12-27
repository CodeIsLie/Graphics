using GlmNet;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Tao.OpenGl;

namespace ModelImporting
{
    public class Lighting
    {
        public class DirLight
        {
            public vec3 Direction { get; set; } = new vec3(0, -1, -1);
            public vec3 Ambient { get; set; } = new vec3(0.05f, 0.05f, 0.05f);
            public vec3 Diffuse { get; set; } = new vec3(255f / 255f / 4f, 222f / 255f / 4f, 173f / 255f / 4f);
            public vec3 Specular { get; set; } = new vec3(0.9f, 0.9f, 0.9f);
        }

        public class PointLight
        {
            public vec3 Ambient { get; set; } = new vec3(0.1f, 0.1f, 0.1f);
            public vec3 Diffuse { get; set; } = new vec3(2, 2, 2);
            public vec3 Specular { get; set; } = new vec3(4, 4, 4);
            public vec3 Position { get; set; } = new vec3(0, 0, 1);

            public float Constant { get; set; } = 1;
            public float Linear { get; set; } = 0.1f;
            public float Quadratic { get; set; } = 0.2f;
        }

        public class SpotLight
        {
            public vec3 Ambient { get; set; } = new vec3(0.0f, 0.0f, 0.0f);
            public vec3 Diffuse { get; set; } = new vec3(2, 2, 2);
            public vec3 Specular { get; set; } = new vec3(4, 4, 4);

            public vec3 Position { get; set; } = new vec3(0, 0, 1);
            public vec3 Direction { get; set; } = new vec3(0, 0, 1);
            public float CutOff { get; set; } = glm.radians(55);

            public float Constant { get; set; } = 1;
            public float Linear { get; set; } = 0.1f;
            public float Quadratic { get; set; } = 0.2f;
        }

        public bool UseFlashlight { get; set; } = false;

        public bool IsOn { get; set; } = true;

        public DirLight DirectionLight { get; set; } = new DirLight();

        public SpotLight FlashLight { get; set; } = new SpotLight();

        public List<PointLight> PointLights { get; set; } = new List<PointLight>();

        public void Setup(uint shader)
        {
            int isOnLoc = Gl.glGetUniformLocation(shader, "isOn");
            Gl.glUniform1i(isOnLoc, IsOn ? 1 : 0);

            int useFlashlightLoc = Gl.glGetUniformLocation(shader, "useFlashlight");
            Gl.glUniform1i(useFlashlightLoc, UseFlashlight ? 1 : 0);

            // dir light
            int ambientColorLoc = Gl.glGetUniformLocation(shader, "dirLight.ambient");
            Gl.glUniform3f(ambientColorLoc,
                DirectionLight.Ambient.x, DirectionLight.Ambient.y, DirectionLight.Ambient.z);

            int diffuseColorLoc = Gl.glGetUniformLocation(shader, "dirLight.diffuse");
            Gl.glUniform3f(diffuseColorLoc,
                DirectionLight.Diffuse.x, DirectionLight.Diffuse.y, DirectionLight.Diffuse.z);

            int specularColorLoc = Gl.glGetUniformLocation(shader, "dirLight.specular");
            Gl.glUniform3f(specularColorLoc,
                DirectionLight.Specular.x, DirectionLight.Specular.y, DirectionLight.Specular.z);

            int lightPosLoc = Gl.glGetUniformLocation(shader, "dirLight.direction");
            Gl.glUniform3f(lightPosLoc,
                DirectionLight.Direction.x, DirectionLight.Direction.y, DirectionLight.Direction.z);

            // point light
            for (int i = 0; i < PointLights.Count; ++i)
            {
                var s = string.Format("pointLights[{0}].position", i);
                int pointPosLoc = Gl.glGetUniformLocation(shader, s);
                Gl.glUniform3f(pointPosLoc,
                    PointLights[i].Position.x, PointLights[i].Position.y, PointLights[i].Position.z);

                int pointAmbientLoc = Gl.glGetUniformLocation(shader, string.Format("pointLights[{0}].ambient", i));
                Gl.glUniform3f(pointAmbientLoc,
                    PointLights[i].Ambient.x, PointLights[i].Ambient.y, PointLights[i].Ambient.z);

                int pointDiffuseLoc = Gl.glGetUniformLocation(shader, string.Format("pointLights[{0}].diffuse", i));
                Gl.glUniform3f(pointDiffuseLoc,
                    PointLights[i].Diffuse.x, PointLights[i].Diffuse.y, PointLights[i].Diffuse.z);

                int pointSpecularLoc = Gl.glGetUniformLocation(shader, string.Format("pointLights[{0}].specular", i));
                Gl.glUniform3f(pointSpecularLoc,
                    PointLights[i].Specular.x, PointLights[i].Specular.y, PointLights[i].Specular.z);

                int pointConstantLoc = Gl.glGetUniformLocation(shader, string.Format("pointLights[{0}].constant", i));
                Gl.glUniform1f(pointConstantLoc, PointLights[i].Constant);

                int pointLinearLoc = Gl.glGetUniformLocation(shader, string.Format("pointLights[{0}].linear", i));
                Gl.glUniform1f(pointLinearLoc, PointLights[i].Linear);

                int pointQuadraticLoc = Gl.glGetUniformLocation(shader, string.Format("pointLights[{0}].quadratic", i));
                Gl.glUniform1f(pointQuadraticLoc, PointLights[i].Quadratic);
            }
            
            int spotPosLoc = Gl.glGetUniformLocation(shader, "spotLight.position");
            Gl.glUniform3f(spotPosLoc,
                FlashLight.Position.x, FlashLight.Position.y, FlashLight.Position.z);

            int spotDirLoc = Gl.glGetUniformLocation(shader, "spotLight.direction");
            Gl.glUniform3f(spotDirLoc,
                FlashLight.Direction.x, FlashLight.Direction.y, FlashLight.Direction.z);

            int spotAmbientLoc = Gl.glGetUniformLocation(shader, "spotLight.ambient");
            Gl.glUniform3f(spotAmbientLoc,
                FlashLight.Ambient.x, FlashLight.Ambient.y, FlashLight.Ambient.z);

            int spotDiffuseLoc = Gl.glGetUniformLocation(shader, "spotLight.diffuse");
            Gl.glUniform3f(spotDiffuseLoc,
                FlashLight.Diffuse.x, FlashLight.Diffuse.y, FlashLight.Diffuse.z);

            int spotSpecularLoc = Gl.glGetUniformLocation(shader, "spotLight.specular");
            Gl.glUniform3f(spotSpecularLoc,
                FlashLight.Specular.x, FlashLight.Specular.y, FlashLight.Specular.z);

            int spotConstantLoc = Gl.glGetUniformLocation(shader, "spotLight.constant");
            Gl.glUniform1f(spotConstantLoc, FlashLight.Constant);

            int spotLinearLoc = Gl.glGetUniformLocation(shader, "spotLight.linear");
            Gl.glUniform1f(spotLinearLoc, FlashLight.Linear);

            int spotQuadraticLoc = Gl.glGetUniformLocation(shader, "spotLight.quadratic");
            Gl.glUniform1f(spotQuadraticLoc, FlashLight.Quadratic);

            int spotCutOffLoc = Gl.glGetUniformLocation(shader, "spotLight.cutOff");
            Gl.glUniform1f(spotCutOffLoc, FlashLight.CutOff);
        }
    }
}
