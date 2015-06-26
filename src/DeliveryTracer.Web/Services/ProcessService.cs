using System.Diagnostics;
using System.IO;
using DeliveryTracer.DataLayer.DataObjects;
using DeliveryTracer.Web.Models;
using DeliveryTracer.Web.Models.Enums;

namespace DeliveryTracer.Web.Services
{
    public class ProcessService
    {
        private static ProcessStartInfo _info;
        private static AppConfigurations _config;
        private static ProcessService _service;

        public static ProcessService CreateProcessInfo(AppConfigurations config)
        {
            _config = config;

            _info = new ProcessStartInfo
            {
                CreateNoWindow = true,
                RedirectStandardError = true,
                RedirectStandardOutput = true,
                UseShellExecute = false,
                FileName = _config.GitPath
            };


            _service = new ProcessService();

            return _service;
        }

        public string Run(GitCommand command, Pipeline model)
        {
            var process = new Process();

            var gitLogRequest = !string.IsNullOrEmpty(model.LastCheckedGitCommitId) ? model.LastCheckedGitCommitId+"^..HEAD" : "-1";

            var commandString = command == GitCommand.Log ? string.Format("{0} {1}", command.ToString().ToLower(), gitLogRequest) : command.ToString().ToLower();

            _info.Arguments = commandString;
            _info.WorkingDirectory = string.Format(_config.RepositoryDirPattern, model.GitFolderName);

            if (command == GitCommand.Clone && !Directory.Exists(_info.WorkingDirectory))
            {
                var directory = _config.RepositoryDirPattern.Replace("{0}", "");
                Directory.CreateDirectory(directory);

                _info.Arguments = commandString + " " + model.GitRepository;
                _info.WorkingDirectory = directory;
            }

            process.StartInfo = _info;
            process.Start();

            var errorString = process.StandardError.ReadToEnd();
            var outputString = process.StandardOutput.ReadToEnd();

            process.WaitForExit();
            process.Close(); 
            process.Dispose();

            return !string.IsNullOrEmpty(errorString) ? errorString : outputString;
        }
    }
}