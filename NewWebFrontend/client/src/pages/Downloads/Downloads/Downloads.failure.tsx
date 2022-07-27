import { TDownloadsFailureProps } from "./Downloads.types";

const DownloadsFailure : React.FC<TDownloadsFailureProps> = () => {
  return (
    <p>There was an error fetching list of downloads. Please try again later...</p>
  );
};

export default DownloadsFailure;
