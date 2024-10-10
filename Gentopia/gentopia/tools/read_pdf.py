from typing import AnyStr
from gentopia.tools.basetool import *
import urllib.request
import PyPDF2
import io

# Define the arguments for the PDF reader tool
class PDFReaderArgs(BaseModel):
    pdf_url: str = Field(..., description="URL link to the PDF file")

# PDFReader class for fetching and reading text from a PDF
class PDFReader(BaseTool):
    name = "pdf_reader"
    description = "Tool for reading and extracting text from a PDF file using a URL input"
    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs

    def _run(self, pdf_url: AnyStr) -> str:
        try:
            # Create a request to retrieve the PDF file from the given URL
            request = urllib.request.Request(pdf_url, headers={'User-Agent': "Mozilla/5.0"})
            # Download the PDF as a binary object
            response = urllib.request.urlopen(request).read()
            # Convert the binary data into a file-like object
            pdf_stream = io.BytesIO(response)
            # Initialize the PDF reader using PyPDF2 to process the file-like object
            pdf_reader = PyPDF2.PdfReader(pdf_stream)
            # Extract and return the text from all the pages in the PDF
            return "\n\n".join(page.extract_text() for page in pdf_reader.pages)
        except Exception as error:
            # Catch and raise an exception if there are issues reading the PDF
            raise ValueError("Unable to retrieve or parse the PDF. Please check the URL.") from error

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    # Test case to demonstrate the usage of the PDFReader class
    pdf_text = PDFReader()._run("https://arxiv.org/pdf/2407.02067")
    print(pdf_text)