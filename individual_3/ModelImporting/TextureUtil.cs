using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Tao.DevIl;
using Tao.OpenGl;

namespace SquareSharpGLScene
{
    public class TextureUtil
    {
        public static int LoadTexture(string texturePath)
        {
            int texture = 0;
            Gl.glEnable(Gl.GL_TEXTURE_2D);

            Gl.glGenTextures(1, out texture);
            Gl.glBindTexture(Gl.GL_TEXTURE_2D, texture);

            Bitmap bitmap = new Bitmap(texturePath);
            BitmapData data = bitmap.LockBits(
                            new Rectangle(0, 0, bitmap.Width, bitmap.Height),
                            ImageLockMode.ReadOnly,
                            PixelFormat.Format24bppRgb);
            Gl.glTexImage2D(Gl.GL_TEXTURE_2D, 0,
                            Gl.GL_RGB, data.Width, data.Height, 0,
                            Gl.GL_BGR, Gl.GL_UNSIGNED_BYTE, data.Scan0);
            bitmap.UnlockBits(data);
            Gl.glTexParameteri(Gl.GL_TEXTURE_2D, Gl.GL_TEXTURE_MIN_FILTER, Gl.GL_LINEAR);
            Gl.glTexParameteri(Gl.GL_TEXTURE_2D, Gl.GL_TEXTURE_MAG_FILTER, Gl.GL_LINEAR);
            Gl.glBindTexture(Gl.GL_TEXTURE_2D, texture);
            return texture;
        }
    }
}
