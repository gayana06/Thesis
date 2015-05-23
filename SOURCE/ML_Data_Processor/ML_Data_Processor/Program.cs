using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ML_Data_Processor
{
    class Program
    {
        private static string path = @"D:\EMDC_IST\SEMESTER_4\Development\NEW-ML-DATA\SKEW-MIX";
        private static string outfile = @"D:\VISUAL_STUDIO\OUTPUT\result.txt";
        private static string patternPerformance = "*performace.txt";
        private static string patternSSBENCH = "*ssbench.txt";
        private static char SEP_DASH = '-';
        private static char SEP_EQUAL = '=';
        private static string TEXT_EXTENSION = ".txt";
        private static bool IS_FIND_MAX_TPT= true;
        private static string SEP_TXT_AVG = "Average requests per second:";



        private static string TXT_ZKZ = "ZKZ";
        private static string TXT_PIPE = "||";
        private static string TXT_START = "**";
        private static string TXT_COMMA = ",";
        private static string TXT_CASE_ID = "CASE-ID";
        private static string TXT_write_quorum = "write_quorum";
        private static string TXT_received_gets = "received_gets";
        private static string TXT_received_puts = "received_puts";
        private static string TXT_get_avg_latency = "get_avg_latency";
        private static string TXT_put_avg_latency = "put_avg_latency";
        private static string TXT_replied_gets = "replied_gets";
        private static string TXT_replied_puts = "replied_puts";

        private static Dictionary<int, string> resultMap;

        static void Main(string[] args)
        {
            resultMap = new Dictionary<int, string>();
            if (IS_FIND_MAX_TPT)
            {
                ProcessMAX();
            }
            else
            {
                Process();
                WriteFile();
            }
            
        }

        private static string NodeMapping(string ip)
        {
            string ssbench = null;
            if (ip == "172.31.0.175")
            {
                ssbench = "172.31.0.170";
            }
            else if (ip == "172.31.0.176")
            {
                ssbench = "172.31.0.171";
            }
            else if (ip == "172.31.0.177")
            {
                ssbench = "172.31.0.172";
            }
            else if (ip == "172.31.0.178")
            {
                ssbench = "172.31.0.173";
            }
            else if (ip == "172.31.0.179")
            {
                ssbench = "172.31.0.174";
            }
            else if (ip == "172.31.0.107")
            {
                ssbench = "172.31.0.5";
            }
            else if (ip == "172.31.0.164")
            {
                ssbench = "172.31.0.169";
            }
            else if (ip == "172.31.0.161")
            {
                ssbench = "172.31.0.106";
            }
            else if (ip == "172.31.0.166")
            {
                ssbench = "172.31.0.163";
            }
            else if (ip == "172.31.0.169")
            {
                ssbench = "172.31.0.168";
            }
            return ssbench;

        }

        private static ML_Record GenerateMLRecord(string[] data,int index)
        {
            ML_Record record = new ML_Record();
            record.Index = index;
            foreach (var item in data)
            {
                if (item.Contains(TXT_CASE_ID))
                {
                    record.CaseID = Int32.Parse(item.Split(SEP_EQUAL)[1]);
                }
                else if (item.Contains(TXT_write_quorum))
                {
                    record.WriteQuorum = Int32.Parse(item.Split(SEP_EQUAL)[1]);
                }
                else if (item.Contains(TXT_received_gets))
                {
                    record.ReceiverdGets = Int32.Parse(item.Split(SEP_EQUAL)[1]);
                }
                else if (item.Contains(TXT_received_puts))
                {
                    record.ReceivedPuts = Int32.Parse(item.Split(SEP_EQUAL)[1]);
                }
                else if (item.Contains(TXT_get_avg_latency))
                {
                    record.AverageGetDuration = float.Parse(item.Split(SEP_EQUAL)[1]);
                }
                else if (item.Contains(TXT_put_avg_latency))
                {
                    record.AveragePutDuration = float.Parse(item.Split(SEP_EQUAL)[1]);
                }
                else if (item.Contains(TXT_replied_gets))
                {
                    record.RepliedGets = Int32.Parse(item.Split(SEP_EQUAL)[1]);
                }
                else if (item.Contains(TXT_replied_puts))
                {
                    record.RepliedPuts = Int32.Parse(item.Split(SEP_EQUAL)[1]);
                }

            }
            if (record.ReceivedPuts < 100 && record.ReceiverdGets < 100)
                record = null;
            else if (record.AveragePutDuration > 1.0 || record.AverageGetDuration > 1.0)
                record = null;
            else if (Math.Abs(record.ReceiverdGets - record.RepliedGets) > 10 || Math.Abs(record.ReceivedPuts - record.RepliedPuts) > 10)
                record = null;
            return record;
        }

        private static void WriteFile()
        {
            StreamWriter writer = null;
            try
            {
                writer = new StreamWriter(outfile);
                var keys = resultMap.Keys.ToList();
                keys.Sort();
                foreach(var key in keys)
                    writer.WriteLine(resultMap[key]);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
            finally
            {
                if (writer != null)
                    writer.Close();
            }
        }

        private static void AverageOutValues(List<ML_Record> mlRecordList)
        {
            if (mlRecordList.Count > 0)
            {
                
                int caseid = mlRecordList.ElementAt(0).CaseID;
                int writeQuorum = mlRecordList.ElementAt(0).WriteQuorum;

                Dictionary<int, Stats> statMap = new Dictionary<int, Stats>();
                StringBuilder sb = new StringBuilder();
                
                foreach (var record in mlRecordList)
                {
                    if (!statMap.ContainsKey(record.Index))
                    {
                        statMap.Add(record.Index, new Stats());
                    }

                    statMap[record.Index].Totalreceivedget += record.ReceiverdGets;
                    statMap[record.Index].Totalreceivedput += record.ReceivedPuts;
                    statMap[record.Index].Totalrepliedget += record.RepliedGets;
                    statMap[record.Index].Totalrepliedput += record.RepliedPuts;
                    statMap[record.Index].Totalgetlatancy = (statMap[record.Index].Totalgetlatancy == 0f || statMap[record.Index].Totalgetlatancy > record.AverageGetDuration) ? record.AverageGetDuration : statMap[record.Index].Totalgetlatancy;
                    statMap[record.Index].Totalputlatency = (statMap[record.Index].Totalputlatency == 0f || statMap[record.Index].Totalputlatency > record.AveragePutDuration) ? record.AveragePutDuration : statMap[record.Index].Totalputlatency;
                }


                

              /*  sb.Append(TXT_CASE_ID + SEP_EQUAL + caseid + TXT_PIPE);
                sb.Append(TXT_write_quorum + SEP_EQUAL + writeQuorum + TXT_PIPE);
                sb.Append(TXT_received_gets + SEP_EQUAL + (statMap.Sum(x => x.Value.Totalreceivedget) / statMap.Count) + TXT_PIPE);
                sb.Append(TXT_received_puts + SEP_EQUAL + (statMap.Sum(x => x.Value.Totalreceivedput) / statMap.Count) + TXT_PIPE);
                sb.Append(TXT_get_avg_latency + SEP_EQUAL + (statMap.Sum(x => x.Value.Totalgetlatancy) / statMap.Count) + TXT_PIPE);
                sb.Append(TXT_put_avg_latency + SEP_EQUAL + (statMap.Sum(x => x.Value.Totalputlatency) / statMap.Count) + TXT_PIPE);
                sb.Append(TXT_replied_gets + SEP_EQUAL + (statMap.Sum(x => x.Value.Totalrepliedget) / statMap.Count) + TXT_PIPE);
                sb.Append(TXT_replied_puts + SEP_EQUAL + (statMap.Sum(x => x.Value.Totalrepliedput) / statMap.Count));
                */
                sb.Append(caseid + TXT_COMMA);
                sb.Append(writeQuorum + TXT_COMMA);
                sb.Append((statMap.Sum(x => x.Value.Totalreceivedget) / statMap.Count) + TXT_COMMA);
                sb.Append((statMap.Sum(x => x.Value.Totalreceivedput) / statMap.Count) + TXT_COMMA);
                sb.Append((statMap.Sum(x => x.Value.Totalgetlatancy) / statMap.Count) + TXT_COMMA);
                sb.Append((statMap.Sum(x => x.Value.Totalputlatency) / statMap.Count) + TXT_COMMA);
                sb.Append((statMap.Sum(x => x.Value.Totalrepliedget) / statMap.Count) + TXT_COMMA);
                sb.Append((statMap.Sum(x => x.Value.Totalrepliedput) / statMap.Count ));
                
                resultMap.Add(caseid, sb.ToString());

            }
        }

        public static void Process()
        {
            if (Directory.Exists(path))
            {
                StreamReader reader = null;
                List<ML_Record> mlRecordList=null;
                int count = 0;
                int filecount = 0;
                int index = 0;
                foreach (var dir in Directory.GetDirectories(path))
                {      
                    mlRecordList=new List<ML_Record>();
                    index = 0;
                    foreach (var file in Directory.GetFiles(dir,patternPerformance))
                    {
                        filecount++;
                        index++;
                        try
                        {
                            Console.WriteLine("File= " + file);
                            reader = new StreamReader(file);
                            string content = reader.ReadToEnd();
                            string[] dataarray = content.Split(TXT_ZKZ.ToCharArray());
                            foreach (string row in dataarray)
                            {
                                if (row.Trim().StartsWith(TXT_PIPE + TXT_CASE_ID))
                                {
                                    string[] keyarray=row.Split(new string[]{TXT_PIPE},StringSplitOptions.RemoveEmptyEntries);
                                    ML_Record record = GenerateMLRecord(keyarray,index);
                                    if (record != null)
                                    {
                                        mlRecordList.Add(record);
                                    }
                                }
                            }

                        }
                        catch (Exception ex)
                        {
                            Console.WriteLine(ex.Message);
                        }      
                    }
                    AverageOutValues(mlRecordList);
                    count += mlRecordList.Count;
                }
                Console.WriteLine("File Count = " + filecount);
                Console.WriteLine("Record Count = "+count);
            }
        }

        public static void ProcessMAX()
        {
            if (Directory.Exists(path))
            {
                StreamReader reader = null;
                string[] folderArray = Directory.GetDirectories(path);
                Dictionary<int, string> pathmap = new Dictionary<int, string>();
                foreach (var item in folderArray)
                {
                    int dirname= Int16.Parse(Path.GetFileName(item));
                    pathmap.Add(dirname, item);
                }
                var keys = pathmap.Keys.ToList();
                keys.Sort();
                float TotalThroughput = 0f;
                float ReadThroughput = 0f;
                float WriteThroughput = 0f;
                int indicator = 1;
                Dictionary<int, float> totalTptMap = new Dictionary<int, float>();
                Dictionary<int, float> readTptMap = new Dictionary<int, float>();
                Dictionary<int, float> writeTptMap = new Dictionary<int, float>();
                foreach (var key in keys)
                { 
                    var dir = pathmap[key];
                    TotalThroughput = 0f;
                    ReadThroughput = 0f;
                    WriteThroughput = 0f;
                    foreach (var file in Directory.GetFiles(dir, patternSSBENCH))
                    {
                        try
                        {
                            Console.WriteLine("File= " + file);
                            reader = new StreamReader(file);
                            string content = reader.ReadToEnd();
                            string[] dataarray = content.Split(new string[]{SEP_TXT_AVG},StringSplitOptions.RemoveEmptyEntries);
                            TotalThroughput += float.Parse(dataarray[1].Substring(0, 7).Trim());
                            if (dataarray.Length == 4)
                            {
                                ReadThroughput += float.Parse(dataarray[2].Substring(0, 7).Trim());
                                WriteThroughput += float.Parse(dataarray[3].Substring(0, 7).Trim());
                            }


                        }
                        catch (Exception ex)
                        {
                            Console.WriteLine(ex.Message);
                        }
                    }
                    indicator++;
                    totalTptMap.Add(key, TotalThroughput);
                    readTptMap.Add(key, ReadThroughput);
                    writeTptMap.Add(key, WriteThroughput);
                }

                foreach (var data in totalTptMap)
                {
                    resultMap.Add(data.Key,data.Key+TXT_COMMA+data.Value+TXT_COMMA+readTptMap[data.Key]+TXT_COMMA+writeTptMap[data.Key]);
                }
                WriteFile();

            }
        }
    }
}
