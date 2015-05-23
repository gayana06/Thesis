using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ML_Data_Processor
{
    class Stats
    {
        int totalreceivedget;

        public int Totalreceivedget
        {
            get { return totalreceivedget; }
            set { totalreceivedget = value; }
        }
        int totalreceivedput;

        public int Totalreceivedput
        {
            get { return totalreceivedput; }
            set { totalreceivedput = value; }
        }
        int totalrepliedget;

        public int Totalrepliedget
        {
            get { return totalrepliedget; }
            set { totalrepliedget = value; }
        }
        int totalrepliedput;

        public int Totalrepliedput
        {
            get { return totalrepliedput; }
            set { totalrepliedput = value; }
        }
        float totalgetlatancy;

        public float Totalgetlatancy
        {
            get { return totalgetlatancy; }
            set { totalgetlatancy = value; }
        }
        float totalputlatency;

        public float Totalputlatency
        {
            get { return totalputlatency; }
            set { totalputlatency = value; }
        }
    }
}
