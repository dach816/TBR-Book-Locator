import { useState } from "react";
import { Button } from "react-bootstrap";

function TruncatedText({truncatedText, fullText}) {
    const [seeMore, setSeeMore] = useState(false);
    if (!truncatedText) {
        return <></>
    }

    return (
        <>
            {!seeMore ? `${truncatedText}...` : fullText}
            <Button variant="link" className="pt-0 pb-1 border border-0" onClick={() => setSeeMore(!seeMore)}>see {seeMore ? 'less' : 'more'}</Button>
        </>
    )
}

export default TruncatedText;