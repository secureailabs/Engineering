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
            Console.WriteLine("Usage: SailDatasetPackager.exe --template <templateFilename> --datasetfilename <datasetFilename> --sailplatformaddress <address> --username <username> --password <password> [--workingfolder <workingFolder>]");
            Console.WriteLine("");
            Console.WriteLine("where:");
            Console.WriteLine("");
            Console.WriteLine("  --template,            A mandatory argument used to specify the input template to be used.");
            Console.WriteLine("  --datasetfilename,     A mandatory argument used to specify the output dataset filename to be used.");
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
            int returnValue = -1;
            DatasetProperties datasetProperties = null;
            NotificationsAndProgressTracker notificationsAndProgressTracker = new NotificationsAndProgressTracker();

            if (0 < arguments.Length)
            {
                // Attach to the current console. Use 0xFFFFFFFF to use the current process
                ApiInterop.AttachConsole(0xFFFFFFFF);

                // Extract the required command line parameters. What we need is
                // the template file, the source csv file and the destination file
                string originalWorkingFolder = System.IO.Directory.GetCurrentDirectory();
                string templateFilename = null;
                string datasetFilename = null;
                string sailPlatformAddress = null;
                string username = null;
                string password = null;
                
                // The index is incremented by the loop, but within the loop, binary arguments require the
                // index to be manually incremented to skip an argument (i.e. the value of a binary argument).
                // Unary arguments don't need that.
                for (int index = 0; index < arguments.Length; index++)
                {
                    if ("--template" == arguments[index].ToLower())
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            templateFilename = arguments[index + 1];
                            index++;
                        }
                    }
                    else if ("--datasetfilename" == arguments[index].ToLower())
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            datasetFilename = arguments[index + 1];
                            index++;
                        }
                    }
                    else if ("--sailplatformaddress" == arguments[index].ToLower())
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            sailPlatformAddress = arguments[index + 1];
                            index++;
                        }
                    }
                    else if ("--username" == arguments[index].ToLower())
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            username = arguments[index + 1];
                            index++;
                        }
                    }
                    else if ("--password" == arguments[index].ToLower())
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            password = arguments[index + 1];
                            index++;
                        }
                    }
                    else if ("--workingfolder" == arguments[index].ToLower())
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

                if ((null == templateFilename)||(null == datasetFilename)||(null == username)||(null == password)||(null == sailPlatformAddress))
                {
                    Console.WriteLine("ERROR: Missing command line parameter(s).");
                    Console.WriteLine("");
                    Program.PrintUsage();
                    Application.Exit();
                }

                // Package up the dataset
                datasetProperties = new DatasetProperties(templateFilename);
                DatasetPackagerCli datasetPackagerCli = new DatasetPackagerCli(ref datasetProperties, ref notificationsAndProgressTracker, datasetFilename);
                datasetPackagerCli.PackageDataset(sailPlatformAddress, username, password);
                returnValue = 0;

                // Restore the original working folder
                System.IO.Directory.SetCurrentDirectory(originalWorkingFolder);
            }
            else
            {
                // Everything is from scratch through the GUI
                datasetProperties = new DatasetProperties();
                Application.EnableVisualStyles();
                Application.SetCompatibleTextRenderingDefault(false);
                //Application.Run(new StructuredBufferTestDialog());
                Application.Run(new MainDialog(ref datasetProperties, ref notificationsAndProgressTracker));
                returnValue = 0;
            }

            return returnValue;
        }
    }
}
