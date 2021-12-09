using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SailTablePackagerForCsv
{
    internal static class Program
    {
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

            if (0 < arguments.Length)
            {
                string templateFilename = null;
                string sourceCsvFile = null;
                string destinationPackage = null;
                string sourceSailTableFile = null;
                string newSailTableFile = null;

                for (int index = 0; index < arguments.Length; index++)
                {
                    if ("--new" == arguments[index])
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            newSailTableFile = arguments[index + 1];
                            index++;
                        }
                    }
                    else if ("--edit" == arguments[index])
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            sourceSailTableFile = arguments[index + 1];
                            index++;
                        }
                    }
                    else if ("--template" == arguments[index])
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            templateFilename = arguments[index + 1];
                            index++;
                        }
                    }
                    else if ("--sourcecsv" == arguments[index])
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            sourceCsvFile = arguments[index + 1];
                            index++;
                        }
                    }
                    else if ("--destinationpackage" == arguments[index])
                    {
                        if ((index + 1) < arguments.Length)
                        {
                            destinationPackage = arguments[index + 1];
                            index++;
                        }
                    }
                }

                // Now that we presumably have all the information we need, let's verify that we have everything that
                // is required
                if ((null != templateFilename) && (null != sourceCsvFile) && (null != destinationPackage))
                {
                    tableProperties = new TableProperties(templateFilename);
                    tableProperties.SourceFilename = sourceCsvFile;
                    TablePackagerCli tablePackagerCli = new TablePackagerCli(ref tableProperties, destinationPackage);
                    step = tablePackagerCli.PackageTable();
                }
                else if (null != newSailTableFile)
                {
                    // Everything is from scratch, but the destination file is already defined
                    tableProperties = new TableProperties();
                    tableProperties.SetTableProperty("DestinationIntermediateFile", newSailTableFile);
                    step = 1;
                    step = InteractiveEngine(ref tableProperties, step);
                }
                else if (null != sourceSailTableFile)
                {
                    // Everything is from scratch, but the destination file is already defined
                    tableProperties = new TableProperties();
                    ///tableProperties.LoadFromIntermediateFile(sourceSailTableFile);
                    step = 3;
                    step = InteractiveEngine(ref tableProperties, step);
                }
            }
            else
            {
                // Everything is from scratch
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
    }
}
