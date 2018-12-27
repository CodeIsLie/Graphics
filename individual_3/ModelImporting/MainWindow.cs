using GlmNet;
using SimpleShaders;
using SquareSharpGLScene;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using Tao.DevIl;
using Tao.FreeGlut;
using Tao.Glfw;
using Tao.OpenGl;

namespace ModelImporting
{
    public partial class MainWindow : Form
    {
        public static float SceneWidth;
        public static float SceneHeight;
        
        private Point lastMousePosition;
        private HashSet<Keys> keys = new HashSet<Keys>();
        private List<RenderObject> renderObjects = new List<RenderObject>();

        private uint lanternShader = 0;
        private uint modelShader = 0;
        private uint procTexturingShader = 0;

        private Projection projection;
        private Camera camera;
        private Lighting lighting;

        public MainWindow()
        {
            InitializeComponent();
            SetEngCulture();
            Glfw.glfwInit();
            Scene.InitializeContexts();
            SceneWidth = Scene.Width;
            SceneHeight = Scene.Height;
        }

        private void SetEngCulture()
        {
            var cultureInfo = CultureInfo.GetCultureInfo("en-GB");
            Thread.CurrentThread.CurrentCulture = cultureInfo;
            Thread.CurrentThread.CurrentUICulture = cultureInfo;
        }

        private void GlInit()
        {
            Glut.glutInit();
            Glut.glutInitDisplayMode(Glut.GLUT_RGB | Glut.GLUT_DOUBLE | Glut.GLUT_DEPTH);

            // инициализация библиотеки openIL 
            Il.ilInit();
            Il.ilEnable(Il.IL_ORIGIN_SET);

            // установка цвета очистки экрана (RGBA) 
            Gl.glClearColor(173/255.0f, 216/255.0f, 230/255.0f, 1);

            // установка порта вывода
            Gl.glViewport(0, 0, Scene.Width, Scene.Height);

            // активация проекционной матрицы 
            Gl.glMatrixMode(Gl.GL_PROJECTION);

            // установка перспективы 
            Gl.glLoadIdentity();
            Glu.gluPerspective(90, Scene.Width / Scene.Height, 1, 1000);

            SceneWidth = Scene.Width;
            SceneHeight = Scene.Height;
            lastMousePosition = new Point((int)SceneWidth / 2, (int)SceneHeight / 2);

            // установка объектно-видовой матрицы 
            Gl.glMatrixMode(Gl.GL_MODELVIEW);
            Gl.glLoadIdentity();

            // начальные настройки OpenGL 
            Gl.glEnable(Gl.GL_DEPTH_TEST);
        }

        private void CreateLanternShader()
        {
            string[] vertShader = new string[]
            {
                ShaderLoader.Load(@"..\..\LanternVert.vert")
            };

            string[] fragShader = new string[]
            {
                ShaderLoader.Load(@"..\..\LanternFrag.frag")
            };

            // Vertex shader
            var vertexShader = (uint)Gl.glCreateShader(Gl.GL_VERTEX_SHADER);
            Gl.glShaderSource(vertexShader, 1, vertShader, null);
            Gl.glCompileShader(vertexShader);

            // Fragment shader
            var fragmentShader = (uint)Gl.glCreateShader(Gl.GL_FRAGMENT_SHADER);
            Gl.glShaderSource(fragmentShader, 1, fragShader, null);
            Gl.glCompileShader(fragmentShader);

            // Compile and use shaders
            lanternShader = (uint)Gl.glCreateProgram();
            Gl.glAttachShader(lanternShader, vertexShader);
            Gl.glAttachShader(lanternShader, fragmentShader);
            Gl.glLinkProgram(lanternShader);

            Gl.glUseProgram(lanternShader);
            Gl.glDeleteShader(fragmentShader);
            Gl.glDeleteShader(vertexShader);
        }

        private void CreateProcTexturingShader()
        {
            string[] vertShader = new string[]
            {
                ShaderLoader.Load(@"..\..\LightingVert.vert")
            };

            string[] fragShader = new string[]
            {
                ShaderLoader.Load(@"..\..\ProcTexturingFrag.frag")
            };

            // Vertex shader
            var vertexShader = (uint)Gl.glCreateShader(Gl.GL_VERTEX_SHADER);
            Gl.glShaderSource(vertexShader, 1, vertShader, null);
            Gl.glCompileShader(vertexShader);

            // Fragment shader
            var fragmentShader = (uint)Gl.glCreateShader(Gl.GL_FRAGMENT_SHADER);
            Gl.glShaderSource(fragmentShader, 1, fragShader, null);
            Gl.glCompileShader(fragmentShader);

            // Compile and use shaders
            procTexturingShader = (uint)Gl.glCreateProgram();
            Gl.glAttachShader(procTexturingShader, vertexShader);
            Gl.glAttachShader(procTexturingShader, fragmentShader);
            Gl.glLinkProgram(procTexturingShader);

            Gl.glUseProgram(procTexturingShader);
            Gl.glDeleteShader(fragmentShader);
            Gl.glDeleteShader(vertexShader);
        }

        private void CreateModelShader()
        {
            var vertShader = new string[]
            { //Gouraud
                ShaderLoader.Load(@"..\..\LightingVert.vert")
            };
            var fragShader = new string[]
            {
                ShaderLoader.Load(@"..\..\LightingFrag.frag")
            };

            // Vertex shader
            var vertexShader = (uint)Gl.glCreateShader(Gl.GL_VERTEX_SHADER);
            Gl.glShaderSource(vertexShader, 1, vertShader, null);
            Gl.glCompileShader(vertexShader);

            // Fragment shader
            var fragmentShader = (uint)Gl.glCreateShader(Gl.GL_FRAGMENT_SHADER);
            Gl.glShaderSource(fragmentShader, 1, fragShader, null);
            Gl.glCompileShader(fragmentShader);

            // Compile and use shaders
            modelShader = (uint)Gl.glCreateProgram();
            Gl.glAttachShader(modelShader, vertexShader);
            Gl.glAttachShader(modelShader, fragmentShader);
            Gl.glLinkProgram(modelShader);

            Gl.glDeleteShader(fragmentShader);
            Gl.glDeleteShader(vertexShader);
        }

        private void Scene_Load(object sender, EventArgs e)
        {
            GlInit();

            CreateLanternShader();
            CreateModelShader();
            CreateProcTexturingShader();

            camera = new Camera(new vec3(0, 0, 2));
            projection = new Projection();
            lighting = new Lighting();

            CreateRoom();

            // nanosuit
            var model = new Model(@"..\..\NanosuitModel\nanosuit.obj", "NanosuitModel");
            mat4 modelMatrix = new mat4(1);
            modelMatrix = glm.scale(modelMatrix, new vec3(0.15f, 0.15f, 0.15f));
            modelMatrix = glm.translate(modelMatrix, new vec3(-28, -6.9f, -18));
            modelMatrix = glm.rotate(modelMatrix, glm.radians(45), new vec3(0, 1, 0));
            Transform transform = new Transform()
            {
                ModelMatrix = modelMatrix
            };
            renderObjects.Add(new RenderObject(model, transform, modelShader));

            // girl
            modelMatrix = new mat4(1);
            modelMatrix = glm.scale(modelMatrix, new vec3(0.01f, 0.01f, 0.01f));
            modelMatrix = glm.translate(modelMatrix, new vec3(300, -100.9f, -45));
            modelMatrix = glm.rotate(modelMatrix, glm.radians(-80), new vec3(0, 1, 0));
            transform = new Transform()
            {
                ModelMatrix = modelMatrix
            };
            model = new Model(@"..\..\Girl\10016_w_Myriam_30k.OBJ", "Girl");
            var texture = (uint)TextureUtil.LoadTexture(@"..\..\Girl\10016_w_Myriam_Body_D_2k.jpg");
            model.SetCustomTexture(texture);
            renderObjects.Add(new RenderObject(model, transform, modelShader));

            // car
            modelMatrix = new mat4(1);
            modelMatrix = glm.scale(modelMatrix, new vec3(0.06f, 0.06f, 0.06f));
            modelMatrix = glm.translate(modelMatrix, new vec3(-23, -16.1f, 18));
            modelMatrix = glm.rotate(modelMatrix, glm.radians(90), new vec3(0, 1, 0));
            transform = new Transform()
            {
                ModelMatrix = modelMatrix
            };
            model = new Model(@"..\..\Car\L200-OBJ.obj", "Car");
            texture = (uint)TextureUtil.LoadTexture(@"..\..\Car\truck_color_clean.jpg");
            model.SetCustomTexture(texture);
            renderObjects.Add(new RenderObject(model, transform, modelShader));

            // lantern
            modelMatrix = new mat4(1);
            modelMatrix = glm.translate(modelMatrix, new vec3(-3, 1.3f, -3.37f));
            transform = new Transform()
            {
                ModelMatrix = modelMatrix
            };
            model = new Model(@"..\..\Lantern\Gamelantern_updated.obj", "Lantern");
            texture = (uint)TextureUtil.LoadTexture(@"..\..\Lantern\Old_lantern_UV_Diffuse.png");
            model.SetCustomTexture(texture);
            renderObjects.Add(new RenderObject(model, transform, modelShader));
            lighting.PointLights.Add(new Lighting.PointLight() { Position = new vec3(-3f, 1.3f, -3.37f) });
            RenderTimer.Start();
        }

        private void CreateRoom()
        {
            var floorTexture = (uint)TextureUtil.LoadTexture(@"..\..\Floor.jpg");
            var specularMap = (uint)TextureUtil.LoadTexture(@"..\..\NoSpecular.jpg");

            var floor = new Plane(floorTexture, specularMap);
            var modelMatrix = new mat4(1);
            modelMatrix = glm.scale(modelMatrix, new vec3(5f, 1f, 3.5f));
            modelMatrix = glm.translate(modelMatrix, new vec3(0, -1, 0));
            modelMatrix = glm.rotate(modelMatrix, glm.radians(-90), new vec3(1, 0, 0));
            var transform = new Transform()
            {
                ModelMatrix = modelMatrix
            };
            renderObjects.Add(new RenderObject(floor, transform, modelShader));

            var wallTexture = (uint)TextureUtil.LoadTexture(@"..\..\Wall.bmp");
            var wall1 = new Plane(wallTexture, specularMap);
            modelMatrix = new mat4(1);
            modelMatrix = glm.scale(modelMatrix, new vec3(5f, 2f, 1f));
            modelMatrix = glm.translate(modelMatrix, new vec3(0, 0.49f, -3.49f));
            transform = new Transform()
            {
                ModelMatrix = modelMatrix
            };
            renderObjects.Add(new RenderObject(wall1, transform, modelShader));

            var wall2 = new Plane(wallTexture, specularMap);
            modelMatrix = new mat4(1);
            modelMatrix = glm.scale(modelMatrix, new vec3(5f, 2f, 1f));
            modelMatrix = glm.translate(modelMatrix, new vec3(0, 0.49f, 3.49f));
            transform = new Transform()
            {
                ModelMatrix = modelMatrix
            };
            renderObjects.Add(new RenderObject(wall2, transform, procTexturingShader));

            var wall3 = new Plane(wallTexture, specularMap);
            modelMatrix = new mat4(1);
            modelMatrix = glm.rotate(modelMatrix, glm.radians(90), new vec3(0, 1, 0));
            modelMatrix = glm.scale(modelMatrix, new vec3(3.5f, 2f, 1f));
            modelMatrix = glm.translate(modelMatrix, new vec3(0, 0.49f, -4.99f));
            transform = new Transform()
            {
                ModelMatrix = modelMatrix
            };
            renderObjects.Add(new RenderObject(wall3, transform, modelShader));

            var wall4 = new Plane(wallTexture, specularMap);
            modelMatrix = new mat4(1);
            modelMatrix = glm.rotate(modelMatrix, glm.radians(-90), new vec3(0, 1, 0));
            modelMatrix = glm.scale(modelMatrix, new vec3(3.5f, 2f, 1f));
            modelMatrix = glm.translate(modelMatrix, new vec3(0, 0.49f, -4.99f));
            transform = new Transform()
            {
                ModelMatrix = modelMatrix
            };
            renderObjects.Add(new RenderObject(wall4, transform, modelShader));
        }

        private void Draw()
        {
            Gl.glClear(Gl.GL_COLOR_BUFFER_BIT | Gl.GL_DEPTH_BUFFER_BIT);
            
            foreach (var renderObject in renderObjects)
            {
                renderObject.Render(camera, projection, lighting);
            }

            DoMovement();
            lighting.FlashLight.Position = camera.Position;
            lighting.FlashLight.Direction = camera.Front;

            Scene.Invalidate();
        }
        
        private void DoMovement()
        {
            if (keys.Contains(Keys.W))
            {
                camera.Position += camera.Speed * camera.Front;
            }
            if (keys.Contains(Keys.S))
            {
                camera.Position -= camera.Speed * camera.Front;
            }
            if (keys.Contains(Keys.A))
            {
                camera.Position -= glm.normalize(glm.cross(camera.Front, camera.Up)) * camera.Speed;
            }
            if (keys.Contains(Keys.D))
            {
                camera.Position += glm.normalize(glm.cross(camera.Front, camera.Up)) * camera.Speed;
            }
            if (keys.Contains(Keys.Q))
            {
                camera.Position -= camera.Speed * camera.Up;
            }
            if (keys.Contains(Keys.E))
            {
                camera.Position += camera.Speed * camera.Up;
            }
        }

        private void RenderTimer_Tick(object sender, EventArgs e)
        {
            Draw();
        }

        private void Scene_KeyUp(object sender, KeyEventArgs e)
        {
            keys.Remove(e.KeyData);
        }

        private void Scene_KeyDown(object sender, KeyEventArgs e)
        {
            keys.Add(e.KeyData);
            if (e.KeyData == Keys.R)
            {
                lighting.IsOn = !lighting.IsOn;
            }
            if (e.KeyData == Keys.F)
            {
                lighting.UseFlashlight = !lighting.UseFlashlight;
            }
        }

        private void Scene_MouseMove(object sender, MouseEventArgs e)
        {
            float xOffset = e.Location.X - lastMousePosition.X;
            float yOffset = lastMousePosition.Y - e.Location.Y;
            lastMousePosition.X = e.Location.X;
            lastMousePosition.Y = e.Location.Y;
            xOffset *= camera.Sensitivity;
            yOffset *= camera.Sensitivity;
            camera.Yaw += xOffset;
            camera.Pitch += yOffset;

            if (camera.Pitch > 89.0f)
            {
                camera.Pitch = 89f;
            }
            if (camera.Pitch < -89f)
            {
                camera.Pitch = -89f;
            }

            var front = new vec3(
                (float)(Math.Cos(glm.radians(camera.Pitch)) * Math.Cos(glm.radians(camera.Yaw))),
                (float)Math.Sin(glm.radians(camera.Pitch)),
                (float)(Math.Cos(glm.radians(camera.Pitch)) * Math.Sin(glm.radians(camera.Yaw))));

            camera.Front = glm.normalize(front);
        }
    }
}
