namespace ModelImporting
{
    partial class MainWindow
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.Scene = new Tao.Platform.Windows.SimpleOpenGlControl();
            this.RenderTimer = new System.Windows.Forms.Timer(this.components);
            this.SuspendLayout();
            // 
            // Scene
            // 
            this.Scene.AccumBits = ((byte)(0));
            this.Scene.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.Scene.AutoCheckErrors = false;
            this.Scene.AutoFinish = false;
            this.Scene.AutoMakeCurrent = true;
            this.Scene.AutoSwapBuffers = true;
            this.Scene.BackColor = System.Drawing.Color.Black;
            this.Scene.ColorBits = ((byte)(32));
            this.Scene.Cursor = System.Windows.Forms.Cursors.Cross;
            this.Scene.DepthBits = ((byte)(16));
            this.Scene.Location = new System.Drawing.Point(16, 15);
            this.Scene.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.Scene.Name = "Scene";
            this.Scene.Size = new System.Drawing.Size(1188, 524);
            this.Scene.StencilBits = ((byte)(0));
            this.Scene.TabIndex = 0;
            this.Scene.Load += new System.EventHandler(this.Scene_Load);
            this.Scene.KeyDown += new System.Windows.Forms.KeyEventHandler(this.Scene_KeyDown);
            this.Scene.KeyUp += new System.Windows.Forms.KeyEventHandler(this.Scene_KeyUp);
            this.Scene.MouseMove += new System.Windows.Forms.MouseEventHandler(this.Scene_MouseMove);
            // 
            // RenderTimer
            // 
            this.RenderTimer.Interval = 30;
            this.RenderTimer.Tick += new System.EventHandler(this.RenderTimer_Tick);
            // 
            // MainWindow
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1220, 554);
            this.Controls.Add(this.Scene);
            this.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.Name = "MainWindow";
            this.Text = "The Room";
            this.WindowState = System.Windows.Forms.FormWindowState.Maximized;
            this.Load += new System.EventHandler(this.MainWindow_Load);
            this.ResumeLayout(false);

        }

        #endregion

        private Tao.Platform.Windows.SimpleOpenGlControl Scene;
        private System.Windows.Forms.Timer RenderTimer;
    }
}

