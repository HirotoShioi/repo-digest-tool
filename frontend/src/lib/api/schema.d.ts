/**
 * This file was auto-generated by openapi-typescript.
 * Do not make direct changes to the file.
 */

export interface paths {
    "/repositories": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Get all repositories
         * @description Get all repositories
         */
        get: operations["get_repositories_repositories_get"];
        /**
         * Update a repository
         * @description Update a repository. If the URL is not provided, all repositories will be updated.
         */
        put: operations["update_repository_repositories_put"];
        /**
         * Clone a repository
         * @description Clone a repository. If the URL is not provided, all repositories will be cloned.
         */
        post: operations["clone_repository_repositories_post"];
        /**
         * Delete all repositories
         * @description Delete all repositories
         */
        delete: operations["delete_all_repositories_repositories_delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/repositories/{author}/{repository_name}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Get a repository
         * @description Get a repository
         */
        get: operations["get_repository_repositories__author___repository_name__get"];
        put?: never;
        post?: never;
        /**
         * Delete a repository
         * @description Delete a repository. If the URL is not provided, all repositories will be deleted.
         */
        delete: operations["delete_repository_repositories__author___repository_name__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/{author}/{repository_name}/summary": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Get a summary of a repository digest
         * @description Get a summary of a repository digest
         */
        get: operations["get_summary_of_repository__author___repository_name__summary_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/digest": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Create a digest of a repository
         * @description Create a digest of a repository. This will create a digest of the repository and return it as a file.
         */
        post: operations["get_digest_of_repository_digest_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/settings": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Settings */
        get: operations["get_settings_settings_get"];
        /** Update Settings */
        put: operations["update_settings_settings_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        /** CloneRepositoryParams */
        CloneRepositoryParams: {
            /**
             * Url
             * @description The URL of the repository to clone
             */
            url: string;
            /**
             * Branch
             * @description The branch to clone
             */
            branch?: string | null;
        };
        /** FileData */
        FileData: {
            /** Name */
            name: string;
            /** Path */
            path: string;
            /** Extension */
            extension: string;
            /** Tokens */
            tokens: number;
        };
        /** FileType */
        FileType: {
            /** Extension */
            extension: string;
            /** Count */
            count: number;
            /** Tokens */
            tokens: number;
        };
        /** GenerateDigestParams */
        GenerateDigestParams: {
            /**
             * Url
             * @description The URL of the repository to create a digest
             */
            url: string;
            /**
             * Branch
             * @description The branch to generate digest for
             */
            branch?: string | null;
        };
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /** Repository */
        Repository: {
            /** Id */
            id: string;
            /** Url */
            url: string;
            /** Branch */
            branch: string | null;
            /**
             * Path
             * Format: path
             */
            path: string;
            /**
             * Updated At
             * Format: date-time
             */
            updated_at: string;
            /** Name */
            name: string;
            /** Author */
            author: string;
            /**
             * Size
             * @default 0
             */
            size: number;
        };
        /** Response */
        Response: {
            /**
             * Status
             * @description The status of the operation
             */
            status: string;
        };
        /** Settings */
        Settings: {
            /**
             * Include Files
             * @description The files to include in the digest
             */
            include_files: string[];
            /**
             * Exclude Files
             * @description The files to exclude from the digest
             */
            exclude_files: string[];
        };
        /** Summary */
        Summary: {
            /** Repository */
            repository: string;
            /** Total Files */
            total_files: number;
            /** Total Size Kb */
            total_size_kb: number;
            /** Average File Size Kb */
            average_file_size_kb: number;
            /** Max File Size Kb */
            max_file_size_kb: number;
            /** Min File Size Kb */
            min_file_size_kb: number;
            /** File Types */
            file_types: components["schemas"]["FileType"][];
            /** Context Length */
            context_length: number;
            /** File Data */
            file_data: components["schemas"]["FileData"][];
        };
        /** UpdateRepositoryParams */
        UpdateRepositoryParams: {
            /**
             * Url
             * @description The URL of the repository to update
             */
            url?: string | null;
            /**
             * Branch
             * @description The branch to update (default: main)
             */
            branch?: string | null;
        };
        /** ValidationError */
        ValidationError: {
            /** Location */
            loc: (string | number)[];
            /** Message */
            msg: string;
            /** Error Type */
            type: string;
        };
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    get_repositories_repositories_get: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Repository"][];
                };
            };
        };
    };
    update_repository_repositories_put: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["UpdateRepositoryParams"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Response"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    clone_repository_repositories_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["CloneRepositoryParams"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Response"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    delete_all_repositories_repositories_delete: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Response"];
                };
            };
        };
    };
    get_repository_repositories__author___repository_name__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                author: string;
                repository_name: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Repository"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    delete_repository_repositories__author___repository_name__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                author: string;
                repository_name: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Response"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_summary_of_repository__author___repository_name__summary_get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                author: string;
                repository_name: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Summary"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_digest_of_repository_digest_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["GenerateDigestParams"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_settings_settings_get: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Settings"];
                };
            };
        };
    };
    update_settings_settings_put: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Settings"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Settings"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
}
