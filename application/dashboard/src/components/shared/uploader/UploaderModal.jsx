import React, { useState } from "react";
import { Modal } from "react-bootstrap";
import { useEffect } from "react";
import "./UploaderModal.scss";
import UploaderPreview from "./UploaderPreview";

const UploaderModal = ({ showModal, file, closeUploaderModal }) => {
    const [show, setShow] = useState(false);

    useEffect(() => {
        setShow(showModal);
    }, [showModal]);

    return (
        <>
            <Modal
                className="UploaderImageModal"
                show={show}
                onHide={closeUploaderModal}
                animation={false}
            >
                <Modal.Header closeButton>
                    <Modal.Title className="ellipse-text">
                        {file?.name}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>{<UploaderPreview file={file} />}</Modal.Body>
            </Modal>
        </>
    );
};

export default UploaderModal;
