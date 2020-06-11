import React, { useState } from "react";
import { Modal, Button } from "react-bootstrap";
import { useEffect } from "react";

const UploaderEditImage = (prop) => {
    const [show, setShow] = useState(false);

    useEffect(() => {
        setShow(prop.showModal);
    }, [prop.showModal]);

    const showPreview = () => {
        if (prop.file) {
            return (
                <img src={prop.file.preview} alt="" />
            );
        }
    };

    return (
        <>
            <Modal
                show={show}
                onHide={prop.closeModalImagePreview}
                animation={false}
            >
                <Modal.Header closeButton>
                    <Modal.Title>Modal title</Modal.Title>
                </Modal.Header>

                <Modal.Body>
                    {showPreview()}
                </Modal.Body>

                <Modal.Footer>
                    <Button
                        variant="secondary"
                        onClick={prop.closeModalImagePreview}
                    >
                        Close
                    </Button>
                    <Button variant="primary">Save changes</Button>
                </Modal.Footer>
            </Modal>
        </>
    );
};

export default UploaderEditImage;
