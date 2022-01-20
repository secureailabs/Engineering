using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SailDatasetPackager
{
    internal static class Program
    {
        /// <summary>
        /// 
        /// </summary>
        static void PrintUsage()
        {
            Console.WriteLine("Usage: SailDatasetPackager.exe --template <templateFilename> [--workingfolder]");
            Console.WriteLine("       SailDatasetPackager.exe --template <templateFilename> --datasetfilename <datasetFilename> --publish --sailplatformaddress <address> --username <username> --password <password> [--workingfolder]");
            Console.WriteLine("");
            Console.WriteLine("where:");
            Console.WriteLine("");
            Console.WriteLine("  --template,            A mandatory binary command line argument used to specify the input template");
            Console.WriteLine("                         to used.");
            Console.WriteLine("  --datasetfilename,     An optional binary command line argument used to specify the name of the");
            Console.WriteLine("                         dataset file used to package the dataset automatically.");
            Console.WriteLine("  --publish,             An optional unary command line argument used to specify whether or not the");
            Console.WriteLine("                         newly packaged dataset should be published to the SAIL Platform automatically.");
            Console.WriteLine("  --sailplatformaddress, An optional binary command line argument that must be specified is --publish");
            Console.WriteLine("                         is used. Represents the SAIL platform address.");
            Console.WriteLine("  --username,            An optional binary command line argument that must be specified is --publish");
            Console.WriteLine("                         is used. Represents the SAIL username used to log into the SAIL Platform.");
            Console.WriteLine("  --password,            An optional binary command line argument that must be specified is --publish");
            Console.WriteLine("                         is used. Represents the SAIL password used to log into the SAIL Platform.");
            Console.WriteLine("  --workingfolder,       An optional binary command line argument used to speficy which directory");
            Console.WriteLine("                         to use when running this application.");
            Console.WriteLine("");
        }

        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static int Main(
            string[] arguments
            )
        {
            DatasetProperties datasetProperties = null;
            NotificationsAndProgressTracker notificationsAndProgressTracker = new NotificationsAndProgressTracker();

            if (0 < arguments.Length)
            {
                ApiInterop.AllocConsole();

                Console.WriteLine("===========================================================================================================");
                Console.WriteLine("SAIL Dataset Packager v1.0");
                Console.WriteLine("Copyright (C) 2021 Secure AI Labs Inc., All Rights Reserved.");
                Console.WriteLine("------------------------------------------------------------------------------------------------------------");
                Console.WriteLine("");

                string templateFilename = null;
                string datasetFilename = null;
                string sailPlatformAddress = null;
                string username = null;
                string password = null;
                bool publishDataset = false;

                // The index is incremented by the loop, but within the loop, binary arguments require the
                // index to be manually incremented to skip an argument (i.e. the value of a binary argument).
                // Unary arguments don't need that.
                for (int index = 0; index < arguments.Length; index++)
                {
                    if ("--template" == arguments[index])
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            templateFilename = arguments[index + 1];
                            index++;
                        }
                    }
                    else if ("--datasetfilename" == arguments[index])
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            datasetFilename = arguments[index + 1];
                            index++;
                        }
                    }
                    else if ("--publish" == arguments[index])
                    {
                        publishDataset = true;
                    }
                    else if ("--sailplatformaddress" == arguments[index])
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            sailPlatformAddress = arguments[index + 1];
                            index++;
                        }
                    }
                    else if ("--username" == arguments[index])
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            username = arguments[index + 1];
                            index++;
                        }
                    }
                    else if ("--password" == arguments[index])
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            password = arguments[index + 1];
                            index++;
                        }
                    }
                    else if ("--workingfolder" == arguments[index])
                    {
                        System.IO.Directory.SetCurrentDirectory(arguments[index + 1]);
                    }
                    else
                    {
                        Console.WriteLine("ERROR: Unknown command line parameters specified.");
                        Console.WriteLine("");
                        Program.PrintUsage();
                        Application.Exit();
                    }
                }

                // First we check for an instant error, which is to specify --publish, but then fail to specify username and password
                if ((true == publishDataset)&&((null == username) || (null == password) || (null == sailPlatformAddress)))
                {
                    Console.WriteLine("ERROR: Missing <address>,<username> or <password> parameters required when the --publish parameter is specified.");
                    Console.WriteLine("");
                }
                else if (null != templateFilename)
                {
                    if (null == datasetFilename)
                    {
                        // A template was specified, but not a datasetFilename. This means that the user 
                        datasetProperties = new DatasetProperties(templateFilename);
                        Application.EnableVisualStyles();
                        Application.SetCompatibleTextRenderingDefault(false);
                        Application.Run(new MainDialog(ref datasetProperties, ref notificationsAndProgressTracker));
                    }
                    else
                    {
                        datasetProperties = new DatasetProperties(templateFilename);
                        DatasetPackagerCli datasetPackagerCli = new DatasetPackagerCli(ref datasetProperties, ref notificationsAndProgressTracker, datasetFilename);
                        datasetPackagerCli.PackageDataset(publishDataset, sailPlatformAddress, username, password);
                        Console.WriteLine("");
                        Console.WriteLine("------------------------------------------------------------------------------------------------------------");
                        Console.WriteLine("Press a key when done");
                        Console.ReadKey();
                    }
                }
                else
                {
                    Console.WriteLine("ERROR: Missing command line parameters.");
                    Console.WriteLine("");
                    Program.PrintUsage();
                }
            }
            else
            {
                // Everything is from scratch
                datasetProperties = new DatasetProperties();
                Application.EnableVisualStyles();
                Application.SetCompatibleTextRenderingDefault(false);
                //Application.Run(new StructuredBufferTestDialog());
                Application.Run(new MainDialog(ref datasetProperties, ref notificationsAndProgressTracker));
            }

            return 0;
        }
    }
}
