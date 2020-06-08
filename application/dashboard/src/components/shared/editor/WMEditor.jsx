import React, { useEffect } from "react";
import { Editor } from "@tinymce/tinymce-react";

const WMEditor = () => {
    useEffect(() => {
        customScrollbar();
    }, []); // eslint-disable-line react-hooks/exhaustive-deps

    const handleEditorChange = (e) => {
        console.log("Content was updated:", e.target.getContent());
    };

    const getFreeHeight = () => {
        const { innerHeight: height } = window;
        return height - 60 - 70;
    };

    const customScrollbar = () => {
        let iframe = document.querySelector(".WMEditor .tox-edit-area iframe");
        let attempts = 0;

        setTimeout(() => {
            if (!iframe && attempts < 1000) {
                iframe = document.querySelector(
                    ".WMEditor .tox-edit-area iframe"
                );
                attempts++;
                if (iframe) {
                    const style = document.createElement("style");
                    style.textContent = `
                    ::-webkit-scrollbar {
                        width: 5px;
                        height: 5px;
                        background: #ccc;
                    }
                    ::-webkit-scrollbar-button {
                        display: none;
                    }
                    ::-webkit-scrollbar-track {
                        background-color: transparent;
                    }
                    ::-webkit-scrollbar-track-piece {
                        background-color: transparent;
                    }
                    ::-webkit-scrollbar-thumb {
                        background: #009efb;
                    }
                    ::-webkit-scrollbar-corner {
                        background-color: transparent;
                    }
                    ::-webkit-resizer {
                        background-color: transparent;
                    }
                    `;
                    iframe.contentDocument.head.appendChild(style);
                } else {
                    customScrollbar();
                }
            }
        }, 10);
    };

    return (
        <div className="WMEditor">
            <Editor
                initialValue="<p>Initial content</p>"
                //apiKey="a4qycjs1cuth7exs6aph6e83vjjwybepsmo1gfn1dguvh09h"
                init={{
                    init_instance_callback: (editor) => {
                        const freeTiny = document.querySelector(
                            ".tox .tox-notification--in"
                        );
                        freeTiny.style.display = "none";
                    },
                    max_height: getFreeHeight(),
                    menubar: false,
                    plugins: [
                        "advlist autolink lists link image media",
                        "charmap print preview anchor help",
                        "searchreplace visualblocks code autoresize",
                        "insertdatetime media table paste wordcount",
                    ],
                    toolbar:
                        "undo redo | formatselect | bold italic | alignleft aligncenter alignright | bullist numlist table | forecolor backcolor | outdent indent | link image media | help",
                    mediaembed_max_width: 450,
                    automatic_uploads: true,
                    file_picker_types: "image",
                    images_upload_url: "http://localhost/",
                    images_upload_handler: function (
                        blobInfo,
                        success,
                        failure
                    ) {
                        setTimeout(function () {
                            /* no matter what you upload, we will turn it into TinyMCE logo :)*/
                            success(
                                "http://moxiecode.cachefly.net/tinymce/v9/images/logo.png"
                            );
                        }, 2000);
                    },
                    language: "pt_BR",
                }}
                onChange={handleEditorChange}
            />
        </div>
    );
};

export default WMEditor;
