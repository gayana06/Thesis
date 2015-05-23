using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ResultProcessor
{
    class Program
    {
        static void Main(string[] args)
        {
            Program p = new Program();
            p.Process();
        }

        private string path = @"D:\EMDC_IST\SEMESTER_4\Development\FINAL-RESULT\NEW-ML\Reconfiguration-Latency\Overhead\changing\uniform\5";
        private string patternPerformance = "*performace.txt";

        private void Process()
        {
            StreamReader read = null;
            StreamWriter write=null;
            StringBuilder sb = null;
            foreach (var file in Directory.GetFiles(path, patternPerformance))
            {
                try
                {
                    read = new StreamReader(file);
                    string line = read.ReadToEnd();
                    string[] parts = line.Split(new string[] { "ZKZ" }, StringSplitOptions.None);
                    sb = new StringBuilder();
                    foreach (var item in parts)
                    {
                        if (item.Contains("Read Tpt"))
                        {
                            string wanted = item.Split(new string[] { "||" }, StringSplitOptions.None)[0];
                            string[] vals = wanted.Trim().Split(new string[] { "=" }, StringSplitOptions.None);
                            string readTpt = vals[1].Split(new string[] { " " }, StringSplitOptions.None)[0];
                            string writeTpt = vals[2];
                            sb.Append(readTpt + "," + writeTpt + "\n");
                        }
                    }
                    write = new StreamWriter(file + "-Result");
                    write.WriteLine(sb.ToString());
                    Console.WriteLine(file);
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                }
                finally
                {
                    if (read != null)
                        read.Close();
                    if (write != null)
                        write.Close();
                }
            }

        }
    }


}
