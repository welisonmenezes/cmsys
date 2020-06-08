import React from "react";
import { Editor } from "@tinymce/tinymce-react";

const WMEditor = () => {
    const handleEditorChange = (e) => {
        console.log("Content was updated:", e.target.getContent());
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
                    height: 500,
                    menubar: false,
                    plugins: [
                        "advlist autolink lists link image media",
                        "charmap print preview anchor help",
                        "searchreplace visualblocks code",
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
                }}
                onChange={handleEditorChange}
            />
        </div>
    );
};

export default WMEditor;
