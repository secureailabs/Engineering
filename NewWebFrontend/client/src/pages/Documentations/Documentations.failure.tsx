import { TDocumentationsFailureProps } from "./Documentations.types";

const DocumentationsFailure : React.FC<TDocumentationsFailureProps> = () => {
  return (
    <p>There was an error fetching list of documentation. Please try again later...</p>
  );
};

export default DocumentationsFailure;
