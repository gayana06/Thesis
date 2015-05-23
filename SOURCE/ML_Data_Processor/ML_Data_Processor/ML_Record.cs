using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ML_Data_Processor
{
    class ML_Record
    {

        private int index;

        public int Index
        {
            get { return index; }
            set { index = value; }
        }

        private int caseID;

        public int CaseID
        {
            get { return caseID; }
            set { caseID = value; }
        }
        private int writeQuorum;

        public int WriteQuorum
        {
            get { return writeQuorum; }
            set { writeQuorum = value; }
        }
        private int receiverdGets;

        public int ReceiverdGets
        {
            get { return receiverdGets; }
            set { receiverdGets = value; }
        }
        private int receivedPuts;

        public int ReceivedPuts
        {
            get { return receivedPuts; }
            set { receivedPuts = value; }
        }
        private float averageGetDuration;

        public float AverageGetDuration
        {
            get { return averageGetDuration; }
            set { averageGetDuration = value; }
        }
        private float averagePutDuration;

        public float AveragePutDuration
        {
            get { return averagePutDuration; }
            set { averagePutDuration = value; }
        }
        private int repliedGets;

        public int RepliedGets
        {
            get { return repliedGets; }
            set { repliedGets = value; }
        }
        private int repliedPuts;

        public int RepliedPuts
        {
            get { return repliedPuts; }
            set { repliedPuts = value; }
        }
    }
}
