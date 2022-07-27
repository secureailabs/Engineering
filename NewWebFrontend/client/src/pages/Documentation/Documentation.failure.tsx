import { TDocumentationFailureProps } from "./Documentation.types";

const DocumentationFailure : React.FC<TDocumentationFailureProps> = () => {
  return (
    <p>There was an error fetching list of documentation. Please try again later...</p>
  );
};

export default DocumentationFailure;
