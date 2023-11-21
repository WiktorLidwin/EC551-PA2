using SkiaSharp;
using SkiaSharp.Views.Desktop;
using System.Drawing;
using System.Windows.Forms;
using Newtonsoft.Json;

public class Lut
{
    public int Layer { get; set; }
    public string Name { get; set; }
    public int ID { get; set; }
    public string Details { get; set; }
    public List<List<string>> Function { get; set; }
    public List<string> Inputs { get; set; }

}

public class RootObject
{
    public int Number_of_LUTs { get; set; }
    public int LutType { get; set; }
    public bool FullyConnected { get; set; }
    public List<object> Partial_arch { get; set; }
    public int Number_of_inputs { get; set; }
    public int Number_of_outputs { get; set; }
    public List<List<List<string>>> Expressions { get; set; }
    public List<Lut> LUTs { get; set; }
}

namespace Program2Display
{
    public partial class Form1 : Form
    {
        private SKBitmap bitmap;
        private int canvasWidth;
        private int canvasHeight;
        private int scrollX;
        private int scrollY;
        private float zoomFactor = 1.0f;
        public Form1()
        {
            InitializeComponent();
            pictureBox1.MouseWheel += (x, e) =>
            {
                int delta = e.Delta;
                float zoomDelta = delta > 0 ? 0.1f : -0.1f;

                // Update the zoom factor
                zoomFactor += zoomDelta;

                // Set minimum and maximum zoom levels if desired
                if (zoomFactor < 0.5f)
                    zoomFactor = 0.5f;
                else if (zoomFactor > 2.0f)
                    zoomFactor = 2.0f;

                // Scale the image based on the zoom factor
                pictureBox1.Refresh();

                
            };
        }
        private void DrawSkiaBitmap()
        {
            var LutWidth = 600;
            var LutHeight = 240;
            //TODO change path if using custom
            string filePath = "D:\\Code\\BU\\EC551\\Program2\\output.json";

            using (StreamReader file = File.OpenText(filePath))
            {
                JsonSerializer serializer = new JsonSerializer();
                RootObject root = (RootObject)serializer.Deserialize(file, typeof(RootObject));

                List<Lut> luts = root.LUTs;
                int max_layer = 0;


                var layersWithCount = luts.GroupBy(obj => obj.Layer)
                               .Select(group => new { Layer = group.Key, Count = group.Count() })
                               .OrderByDescending(layer => layer.Count);
                var layerWithMostElements = layersWithCount.FirstOrDefault();
                canvasWidth = 800 * luts.Max(l => l.Layer);
                canvasHeight = 600 * layerWithMostElements.Count;
                

                bitmap = new SKBitmap(canvasWidth, canvasHeight);


                int current_layer = 0;
                int count = 0;
                int ycount = 0;
                while(count  < luts.Count)
                {
                    foreach (Lut lut in luts)
                    {
                        if (lut.Layer == current_layer)
                        {
                            var details = "";
                            if (lut.Function != null)
                            {
                                foreach (var term in lut.Function)
                                {
                                    var lit = "";
                                    foreach (var literal in term)
                                    {
                                        lit += literal;
                                    }
                                    details += lit + " + ";
                                }
                                details = details.Substring(0, details.Length - 3);
                            }
                            
                            var tempLut = new LUT4()
                            {
                                Name = lut.Name,
                                Function = new List<int> { 0},
                                Details = details,
                                Inputs = lut.Inputs
                            };
                            

                            using (SKCanvas canvas = new SKCanvas(bitmap))
                            {
                                canvas.DrawBitmap(tempLut.CreateVisual(LutWidth, LutHeight), LutWidth * current_layer, (LutHeight + 20) * ycount);

                            }
                            ycount ++;
                            count++;
                        }
                        //Console.WriteLine("Name: " + lut.Name);
                        //Console.WriteLine("ID: " + lut.ID);
                        //Console.WriteLine("Details: " + lut.Details);
                        //Console.WriteLine("Function: " + string.Join(", ", lut.Function));
                        //Console.WriteLine();
                    }
                    current_layer++;
                    ycount = 0;
                }
                
            }

            //var lut1 = new LUT4()
            //{
            //    Name = "LUT 1",
            //    Function = new List<int> { 0, 1, 2, 3, 6, 7, 8, 10, 11, 12, 14 },
            //    Inputs = new List<string> { "a", "b", "c", "dd",}
            //};
            //var lut2 = new LUT4()
            //{
            //    Name = "LUT 2",
            //    Function = new List<int> { 0, 1, 2, 3, 6, 7, 8, 10, 11, 12, 14 },
            //    Inputs = new List<string> { "a", "b", "c", "dd", }
            //};
            //var lut3 = new LUT4()
            //{
            //    Name = "LUT 3",
            //    Function = new List<int> { 0, 1, 2, 3, 6, 7, 8, 10, 11, 12, 14 },
            //    Inputs = new List<string> { "a", "b", "c", "dd", }
            //};
            //var lut4 = new LUT4()
            //{
            //    Name = "LUT 4",
            //    Function = new List<int> { 0, 1, 2, 3, 6, 7, 8, 10, 11, 12, 14 },
            //    Inputs = new List<string> { "a", "b", "c", "dd", }
            //};
            

            //canvas.DrawBitmap(lut1.CreateVisual(LutWidth, LutHeight), 0, 0);
            //canvas.DrawBitmap(lut2.CreateVisual(LutWidth, LutHeight), 0, LutHeight + 20);
            //canvas.DrawBitmap(lut3.CreateVisual(LutWidth, LutHeight), 0, LutHeight*2 + 40);
            //canvas.DrawBitmap(lut4.CreateVisual(LutWidth, LutHeight), LutWidth, 0);



        }

        private void Form1_Load(object sender, EventArgs e)
        {
            scrollX = 0;
            scrollY = 0;

            DrawSkiaBitmap();
            // Set the scroll bar properties
            hScrollBar1.Minimum = 0;
            hScrollBar1.Maximum = canvasWidth;
            hScrollBar1.SmallChange = 10;
            hScrollBar1.LargeChange = 100;
            hScrollBar1.Value = 0;

            vScrollBar1.Minimum = 0;
            vScrollBar1.Maximum = canvasHeight;
            vScrollBar1.SmallChange = 10;
            vScrollBar1.LargeChange = 100;
            vScrollBar1.Value = 0;

            // Hook up event handlers for the scroll bars
            //hScrollBar1.ValueChanged += HScrollBar1_ValueChanged;
            //vScrollBar1.ValueChanged += VScrollBar1_ValueChanged;
        }

        private void pictureBox1_LoadCompleted(object sender, System.ComponentModel.AsyncCompletedEventArgs e)
        {

        }

        private void pictureBox1_Paint(object sender, PaintEventArgs e)
        {
            //using (var g = e.Graphics)
            //{
            //    g.DrawImage(bitmap.ToBitmap(), -scrollX, -scrollY);
            //}



            //var tempbitmap = new SKBitmap( (int)(canvasWidth * zoomFactor), (int)(canvasHeight * zoomFactor));
            var tempbitmap = new SKBitmap(canvasWidth, canvasHeight);
            using (SKCanvas canvas = new SKCanvas(tempbitmap))
            {
                canvas.Scale(zoomFactor, zoomFactor);
                canvas.DrawBitmap(bitmap, -scrollX, -scrollY);
            }
            var sysBitmap = tempbitmap.ToBitmap();
            pictureBox1.SizeMode = PictureBoxSizeMode.AutoSize;
            pictureBox1.Image = sysBitmap;
        }

        private void vScrollBar1_ValueChanged(object sender, EventArgs e)
        {
            Console.WriteLine("V changed");
            scrollY = vScrollBar1.Value;
            pictureBox1.Refresh();
        }

        private void hScrollBar1_Scroll(object sender, ScrollEventArgs e)
        {
            Console.WriteLine("h2 changed");
            scrollX = hScrollBar1.Value;
            pictureBox1.Refresh();
        }

        private void hScrollBar1_ValueChanged(object sender, EventArgs e)
        {
            Console.WriteLine("h changed");
            scrollX = hScrollBar1.Value;
            pictureBox1.Refresh();
        }

        private void vScrollBar1_Scroll(object sender, ScrollEventArgs e)
        {
            Console.WriteLine("V2 changed");
            scrollY = vScrollBar1.Value;
            pictureBox1.Refresh();
        }

        private void Form1_Scroll(object sender, ScrollEventArgs e)
        {
            if (e.ScrollOrientation == ScrollOrientation.HorizontalScroll)
            {
                scrollX = e.NewValue;
            }
            else
            {
                scrollY = e.NewValue;
            }

            pictureBox1.Refresh();
        }

        private bool isDragging;
        private Point mouseDownLocation;

        private void pictureBox1_MouseDown(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                isDragging = true;
                mouseDownLocation = e.Location;
                mouseDownLocation.X += scrollX;
                mouseDownLocation.Y += scrollY;

            }
        }

        private void pictureBox1_MouseUp(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                isDragging = false;
            }

        }

        private void pictureBox1_MouseMove(object sender, MouseEventArgs e)
        {
            if (isDragging)
            {
                int dx = e.X - mouseDownLocation.X;
                int dy = e.Y - mouseDownLocation.Y;
                scrollX = -dx;
                scrollY = -dy;
                //Update the PictureBox control's location
                //pictureBox.Location = new Point(pictureBox.Left + dx, pictureBox.Top + dy);
                pictureBox1.Refresh();
            }
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }
    }
    public class LUT4
    {
        public string Name { get; set; }
        public List<string> Inputs { get; set; }
        public List<int> Function { get; set; }

        public string Details { get; set; }

        public SKBitmap CreateVisual(int width, int height)
        {
            var bitmap = new SKBitmap(width, height);

            using (SKCanvas canvas = new SKCanvas(bitmap))
            {
                float rectWidth = width - 200f;
                float rectHeight = height * 1f;
                float rectX = (width - rectWidth);
                float rectY = (height - rectHeight) / 2;

                // Draw the rectangle
                using (SKPaint paint = new SKPaint())
                {
                    paint.Color = SKColors.Black;
                    paint.IsAntialias = true;
                    paint.Style = SKPaintStyle.Stroke;
                    paint.StrokeWidth = 5; // Set the border width

                    SKRect rect = new SKRect(rectX, rectY, rectX + rectWidth, rectY + rectHeight);
                    canvas.DrawRect(rect, paint);
                }



                // Draw the text in the rectangle
                using (SKPaint paint = new SKPaint())
                {
                    paint.TextSize = 36;
                    paint.IsAntialias = true;
                    paint.Color = SKColors.Black;

                    string textTop = Name;
                    float textTopX = rectX + (rectWidth - paint.MeasureText(textTop)) / 2;
                    float textTopY = rectY + paint.TextSize;
                    canvas.DrawText(textTop, textTopX, textTopY, paint);



                    if (Function.Count > 8)
                    {
                        Function.Sort();
                        string textBody = string.Join(", ", Function.GetRange(0, Function.Count/2));
                        float textBodyX = rectX + (rectWidth - paint.MeasureText(textBody)) / 2;
                        float textBodyY = rectY + rectHeight *2 / 3 - paint.TextSize;
                        canvas.DrawText(textBody, textBodyX, textBodyY, paint);

                         textBody = string.Join(", ", Function.GetRange(Function.Count / 2, Function.Count- Function.Count / 2));
                         textBodyX = rectX + (rectWidth - paint.MeasureText(textBody)) / 2;
                         textBodyY = rectY + rectHeight * 2 / 3 + paint.TextSize - 5;
                        canvas.DrawText(textBody, textBodyX, textBodyY, paint);
                    }
                    else
                    {
                        //"0, 1, 2, 3, 6, 7, 8, 9"
                        string textBody = string.Join(", ", Function);
                        textBody = Details;
                        //"10, 11, 12, 13, 14, 15, 16, 17, 18"
                        float textBodyX = rectX + (rectWidth - paint.MeasureText(textBody)) / 2;
                        float textBodyY = rectY + rectHeight / 2 + paint.TextSize;
                        canvas.DrawText(textBody, textBodyX, textBodyY, paint);
                    }

                    
                }

                // Draw the four straight lines
                using (SKPaint paint = new SKPaint())
                {
                    paint.Style = SKPaintStyle.Stroke;
                    paint.IsAntialias = true;
                    paint.Color = SKColors.Black;
                    paint.StrokeWidth = 5;

                    float lineStartX = rectX;
                    float lineEndX = lineStartX - 60;
                    float lineY = rectY + rectHeight / 2;

                    canvas.DrawLine(lineStartX, rectY + rectHeight / 8 + rectHeight * 0/ 4, lineEndX, rectY + rectHeight / 8 + rectHeight * 0 / 4, paint);
                    canvas.DrawLine(lineStartX, rectY + rectHeight / 8 + rectHeight * 1 / 4, lineEndX, rectY + rectHeight / 8 + rectHeight * 1 / 4, paint);
                    canvas.DrawLine(lineStartX, rectY + rectHeight / 8 + rectHeight * 2 / 4, lineEndX, rectY + rectHeight / 8 + rectHeight * 2 / 4, paint);
                    canvas.DrawLine(lineStartX, rectY + rectHeight / 8 + rectHeight * 3 / 4, lineEndX, rectY + rectHeight / 8 + rectHeight * 3 / 4, paint);


                    //canvas.DrawLine(lineStartX, lineY - 20, lineStartX, lineY + 20, paint);
                    //canvas.DrawLine(lineEndX, lineY - 20, lineEndX, lineY + 20, paint);
                }

                using (SKPaint paint = new SKPaint())
                {
                    paint.TextSize = 20;
                    paint.IsAntialias = true;
                    paint.Color = SKColors.Black;

                    //List<string> inputs = new List<string> { "a", "b", "c", "d" };
                    int i = 0;
                    foreach (var input in Inputs)
                    {

                        float textTopX = rectX + (-60 - 5 - paint.MeasureText(input));
                        float textTopY = rectY + rectHeight / 8 + rectHeight * i / 4;
                        canvas.DrawText(input, textTopX, textTopY, paint);
                        i++;
                    }
                }
            }
            return bitmap;
            
        }

    }
    public class LUT6
    {
        public string Name { get; set; }
        public int Age { get; set; }

    }
}