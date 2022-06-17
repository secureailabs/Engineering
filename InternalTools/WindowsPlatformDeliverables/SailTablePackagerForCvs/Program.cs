using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Reflection;
using System.Windows.Forms;

namespace SailTablePackagerForCsv
{
    internal static class Program
    {
        /// <summary>
        /// 
        /// </summary>
        static void PrintUsage()
        {
            Console.WriteLine("Usage: SailTablePackagerForCsv.exe --template <templateFilename> --sourcecsv <sourceCsv> --destinationfile <destinationFile> [--workingfolder <workingFolder>]");
            Console.WriteLine("");
            Console.WriteLine("where:");
            Console.WriteLine("");
            Console.WriteLine("  --template,            A mandatory argument used to specify the input template to be used.");
            Console.WriteLine("  --sourcecsv,           A mandatory argument used to specify which CSV file to get the data from.");
            Console.WriteLine("  --destinationFile,     A mandatory argument used to specify the name of the output sailtable to generate");
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
            int step = 1;
            TableProperties tableProperties = null;

            // Extract the assembly title from the running assembly
            System.Reflection.Assembly assembly = System.Reflection.Assembly.GetExecutingAssembly();
            AssemblyTitleAttribute titleAttribute = (AssemblyTitleAttribute) assembly.GetCustomAttribute(typeof(AssemblyTitleAttribute));
            m_AssemblyTitle = titleAttribute.Title;

            // If there are arguments, then someone is running the application from the command
            // line. Let's extract command line arguments
            if (0 < arguments.Length)
            {
                // Attach to the current console. Use 0xFFFFFFFF to use the current process
                ApiInterop.AttachConsole(0xFFFFFFFF);

                // Extract the required command line parameters. What we need is
                // the template file, the source csv file and the destination file
                string originalWorkingFolder = System.IO.Directory.GetCurrentDirectory();
                string templateFilename = null;
                string sourceCsvFile = null;
                string destinationFile = null;

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
                    else if ("--sourcecsv" == arguments[index].ToLower())
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            sourceCsvFile = arguments[index + 1];
                            index++;
                        }
                    }
                    else if ("--destinationfile" == arguments[index].ToLower())
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            destinationFile = arguments[index + 1];
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

                // Check to make sure we have all of our command line parameters
                if ((null == templateFilename)||(null == sourceCsvFile)||(null == destinationFile))
                {
                    Console.WriteLine("ERROR: Missing command line parameter(s).");
                    Console.WriteLine("");
                    Program.PrintUsage();
                    Application.Exit();
                }

                // Package up the table
                tableProperties = new TableProperties(templateFilename);
                tableProperties.SourceFilename = sourceCsvFile;
                TablePackagerCli tablePackagerCli = new TablePackagerCli(ref tableProperties, destinationFile);
                tablePackagerCli.PackageTable();
                Console.WriteLine("Done packaging " + destinationFile);
                // The CLI return code for when things work is 0
                step = 0;

                // Restore the original working folder
                System.IO.Directory.SetCurrentDirectory(originalWorkingFolder);
            }
            else
            {
                // Use the GUI
                tableProperties = new TableProperties();
                step = 1;
                step = InteractiveEngine(ref tableProperties, step);
            }

            return step;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        static int InteractiveEngine(
            ref TableProperties tableProperties,
            int startingStep
            )
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            int step = startingStep;

            do
            {
                if (1 == step)
                {
                    FileSelectionDialog fileSelectionDialog = new FileSelectionDialog();
                    if (DialogResult.OK == fileSelectionDialog.ShowDialog())
                    {
                        if (0 < fileSelectionDialog.TemplateFilename.Length)
                        {
                            tableProperties = new TableProperties(fileSelectionDialog.TemplateFilename);
                        }
                        tableProperties.SourceFilename = fileSelectionDialog.CsvFilename;
                        step = 2;
                    }
                    else
                    {
                        step = 10;
                    }
                }
                else if (2 == step)
                {
                    GlobalImportPropertiesDialog globalImportPropertiesDialog = new GlobalImportPropertiesDialog(ref tableProperties);
                    if (DialogResult.OK == globalImportPropertiesDialog.ShowDialog())
                    {
                        step = 3;
                    }
                    else
                    {
                        tableProperties.Clear();
                        step = 1;
                    }
                }
                else if (3 == step)
                {
                    TableEditDialog tableEditDialog = new TableEditDialog(ref tableProperties);
                    if (DialogResult.OK == tableEditDialog.ShowDialog())
                    {
                        step = 4;
                    }
                    else
                    {
                        step = 2;
                    }
                }
                else if (4 == step)
                {
                    TablePackagerDialog packageTableDialog = new TablePackagerDialog(ref tableProperties);
                    if (DialogResult.OK == packageTableDialog.ShowDialog())
                    {
                        step = 15;
                    }
                    else
                    {
                        step = 10;
                    }
                }
            }
            while (10 > step);

            return step;
        }

        static public string m_AssemblyTitle;
    }
}
