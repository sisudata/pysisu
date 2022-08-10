# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: options/annotations.proto, options/openapiv2.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import (
    Dict,
    List,
)

import betterproto
import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf


class Scheme(betterproto.Enum):
    """
    Scheme describes the schemes supported by the OpenAPI Swagger and Operation
    objects.
    """

    UNKNOWN = 0
    HTTP = 1
    HTTPS = 2
    WS = 3
    WSS = 4


class JsonSchemaJsonSchemaSimpleTypes(betterproto.Enum):
    UNKNOWN = 0
    ARRAY = 1
    BOOLEAN = 2
    INTEGER = 3
    NULL = 4
    NUMBER = 5
    OBJECT = 6
    STRING = 7


class SecuritySchemeType(betterproto.Enum):
    """
    The type of the security scheme. Valid values are "basic", "apiKey" or
    "oauth2".
    """

    TYPE_INVALID = 0
    TYPE_BASIC = 1
    TYPE_API_KEY = 2
    TYPE_OAUTH2 = 3


class SecuritySchemeIn(betterproto.Enum):
    """The location of the API key. Valid values are "query" or "header"."""

    IN_INVALID = 0
    IN_QUERY = 1
    IN_HEADER = 2


class SecuritySchemeFlow(betterproto.Enum):
    """
    The flow used by the OAuth2 security scheme. Valid values are "implicit",
    "password", "application" or "accessCode".
    """

    FLOW_INVALID = 0
    FLOW_IMPLICIT = 1
    FLOW_PASSWORD = 2
    FLOW_APPLICATION = 3
    FLOW_ACCESS_CODE = 4


@dataclass(eq=False, repr=False)
class Swagger(betterproto.Message):
    """
    `Swagger` is a representation of OpenAPI v2 specification's Swagger object.
    See: https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#swaggerObject Example:  option
    (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_swagger) = {    info:
    {      title: "Echo API";      version: "1.0";      description: "";
    contact: {        name: "gRPC-Gateway project";        url:
    "https://github.com/grpc-ecosystem/grpc-gateway";        email:
    "none@example.com";      };      license: {        name: "BSD 3-Clause
    License";        url: "https://github.com/grpc-ecosystem/grpc-
    gateway/blob/master/LICENSE.txt";      };    };    schemes: HTTPS;
    consumes: "application/json";    produces: "application/json";  };
    """

    swagger: str = betterproto.string_field(1)
    """
    Specifies the OpenAPI Specification version being used. It can be used by
    the OpenAPI UI and other clients to interpret the API listing. The value
    MUST be "2.0".
    """

    info: "Info" = betterproto.message_field(2)
    """
    Provides metadata about the API. The metadata can be used by the clients if
    needed.
    """

    host: str = betterproto.string_field(3)
    """
    The host (name or ip) serving the API. This MUST be the host only and does
    not include the scheme nor sub-paths. It MAY include a port. If the host is
    not included, the host serving the documentation is to be used (including
    the port). The host does not support path templating.
    """

    base_path: str = betterproto.string_field(4)
    """
    The base path on which the API is served, which is relative to the host. If
    it is not included, the API is served directly under the host. The value
    MUST start with a leading slash (/). The basePath does not support path
    templating. Note that using `base_path` does not change the endpoint paths
    that are generated in the resulting OpenAPI file. If you wish to use
    `base_path` with relatively generated OpenAPI paths, the `base_path` prefix
    must be manually removed from your `google.api.http` paths and your code
    changed to serve the API from the `base_path`.
    """

    schemes: List["Scheme"] = betterproto.enum_field(5)
    """
    The transfer protocol of the API. Values MUST be from the list: "http",
    "https", "ws", "wss". If the schemes is not included, the default scheme to
    be used is the one used to access the OpenAPI definition itself.
    """

    consumes: List[str] = betterproto.string_field(6)
    """
    A list of MIME types the APIs can consume. This is global to all APIs but
    can be overridden on specific API calls. Value MUST be as described under
    Mime Types.
    """

    produces: List[str] = betterproto.string_field(7)
    """
    A list of MIME types the APIs can produce. This is global to all APIs but
    can be overridden on specific API calls. Value MUST be as described under
    Mime Types.
    """

    responses: Dict[str, "Response"] = betterproto.map_field(
        10, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    """
    An object to hold responses that can be used across operations. This
    property does not define global responses for all operations.
    """

    security_definitions: "SecurityDefinitions" = betterproto.message_field(11)
    """
    Security scheme definitions that can be used across the specification.
    """

    security: List["SecurityRequirement"] = betterproto.message_field(12)
    """
    A declaration of which security schemes are applied for the API as a whole.
    The list of values describes alternative security schemes that can be used
    (that is, there is a logical OR between the security requirements).
    Individual operations can override this definition.
    """

    external_docs: "ExternalDocumentation" = betterproto.message_field(14)
    """Additional external documentation."""

    extensions: Dict[
        str, "betterproto_lib_google_protobuf.Value"
    ] = betterproto.map_field(15, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)


@dataclass(eq=False, repr=False)
class Operation(betterproto.Message):
    """
    `Operation` is a representation of OpenAPI v2 specification's Operation
    object. See: https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#operationObject Example:  service
    EchoService {    rpc Echo(SimpleMessage) returns (SimpleMessage) {
    option (google.api.http) = {        get: "/v1/example/echo/{id}"      };
    option (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_operation) = {
    summary: "Get a message.";        operation_id: "getMessage";        tags:
    "echo";        responses: {          key: "200"            value: {
    description: "OK";          }        }      };    }  }
    """

    tags: List[str] = betterproto.string_field(1)
    """
    A list of tags for API documentation control. Tags can be used for logical
    grouping of operations by resources or any other qualifier.
    """

    summary: str = betterproto.string_field(2)
    """
    A short summary of what the operation does. For maximum readability in the
    swagger-ui, this field SHOULD be less than 120 characters.
    """

    description: str = betterproto.string_field(3)
    """
    A verbose explanation of the operation behavior. GFM syntax can be used for
    rich text representation.
    """

    external_docs: "ExternalDocumentation" = betterproto.message_field(4)
    """Additional external documentation for this operation."""

    operation_id: str = betterproto.string_field(5)
    """
    Unique string used to identify the operation. The id MUST be unique among
    all operations described in the API. Tools and libraries MAY use the
    operationId to uniquely identify an operation, therefore, it is recommended
    to follow common programming naming conventions.
    """

    consumes: List[str] = betterproto.string_field(6)
    """
    A list of MIME types the operation can consume. This overrides the consumes
    definition at the OpenAPI Object. An empty value MAY be used to clear the
    global definition. Value MUST be as described under Mime Types.
    """

    produces: List[str] = betterproto.string_field(7)
    """
    A list of MIME types the operation can produce. This overrides the produces
    definition at the OpenAPI Object. An empty value MAY be used to clear the
    global definition. Value MUST be as described under Mime Types.
    """

    responses: Dict[str, "Response"] = betterproto.map_field(
        9, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    """
    The list of possible responses as they are returned from executing this
    operation.
    """

    schemes: List["Scheme"] = betterproto.enum_field(10)
    """
    The transfer protocol for the operation. Values MUST be from the list:
    "http", "https", "ws", "wss". The value overrides the OpenAPI Object
    schemes definition.
    """

    deprecated: bool = betterproto.bool_field(11)
    """
    Declares this operation to be deprecated. Usage of the declared operation
    should be refrained. Default value is false.
    """

    security: List["SecurityRequirement"] = betterproto.message_field(12)
    """
    A declaration of which security schemes are applied for this operation. The
    list of values describes alternative security schemes that can be used
    (that is, there is a logical OR between the security requirements). This
    definition overrides any declared top-level security. To remove a top-level
    security declaration, an empty array can be used.
    """

    extensions: Dict[
        str, "betterproto_lib_google_protobuf.Value"
    ] = betterproto.map_field(13, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)


@dataclass(eq=False, repr=False)
class Header(betterproto.Message):
    """
    `Header` is a representation of OpenAPI v2 specification's Header object.
    See: https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#headerObject
    """

    description: str = betterproto.string_field(1)
    """`Description` is a short description of the header."""

    type: str = betterproto.string_field(2)
    """
    The type of the object. The value MUST be one of "string", "number",
    "integer", or "boolean". The "array" type is not supported.
    """

    format: str = betterproto.string_field(3)
    """`Format` The extending format for the previously mentioned type."""

    default: str = betterproto.string_field(6)
    """
    `Default` Declares the value of the header that the server will use if none
    is provided. See: https://tools.ietf.org/html/draft-fge-json-schema-
    validation-00#section-6.2. Unlike JSON Schema this value MUST conform to
    the defined type for the header.
    """

    pattern: str = betterproto.string_field(13)
    """
    'Pattern' See https://tools.ietf.org/html/draft-fge-json-schema-
    validation-00#section-5.2.3.
    """


@dataclass(eq=False, repr=False)
class Response(betterproto.Message):
    """
    `Response` is a representation of OpenAPI v2 specification's Response
    object. See: https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#responseObject
    """

    description: str = betterproto.string_field(1)
    """
    `Description` is a short description of the response. GFM syntax can be
    used for rich text representation.
    """

    schema: "Schema" = betterproto.message_field(2)
    """
    `Schema` optionally defines the structure of the response. If `Schema` is
    not provided, it means there is no content to the response.
    """

    headers: Dict[str, "Header"] = betterproto.map_field(
        3, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    """
    `Headers` A list of headers that are sent with the response. `Header` name
    is expected to be a string in the canonical format of the MIME header key
    See: https://golang.org/pkg/net/textproto/#CanonicalMIMEHeaderKey
    """

    examples: Dict[str, str] = betterproto.map_field(
        4, betterproto.TYPE_STRING, betterproto.TYPE_STRING
    )
    """
    `Examples` gives per-mimetype response examples. See:
    https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#example-object
    """

    extensions: Dict[
        str, "betterproto_lib_google_protobuf.Value"
    ] = betterproto.map_field(5, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)


@dataclass(eq=False, repr=False)
class Info(betterproto.Message):
    """
    `Info` is a representation of OpenAPI v2 specification's Info object. See:
    https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#infoObject Example:  option
    (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_swagger) = {    info:
    {      title: "Echo API";      version: "1.0";      description: "";
    contact: {        name: "gRPC-Gateway project";        url:
    "https://github.com/grpc-ecosystem/grpc-gateway";        email:
    "none@example.com";      };      license: {        name: "BSD 3-Clause
    License";        url: "https://github.com/grpc-ecosystem/grpc-
    gateway/blob/master/LICENSE.txt";      };    };    ...  };
    """

    title: str = betterproto.string_field(1)
    """The title of the application."""

    description: str = betterproto.string_field(2)
    """
    A short description of the application. GFM syntax can be used for rich
    text representation.
    """

    terms_of_service: str = betterproto.string_field(3)
    """The Terms of Service for the API."""

    contact: "Contact" = betterproto.message_field(4)
    """The contact information for the exposed API."""

    license: "License" = betterproto.message_field(5)
    """The license information for the exposed API."""

    version: str = betterproto.string_field(6)
    """
    Provides the version of the application API (not to be confused with the
    specification version).
    """

    extensions: Dict[
        str, "betterproto_lib_google_protobuf.Value"
    ] = betterproto.map_field(7, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)


@dataclass(eq=False, repr=False)
class Contact(betterproto.Message):
    """
    `Contact` is a representation of OpenAPI v2 specification's Contact object.
    See: https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#contactObject Example:  option
    (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_swagger) = {    info:
    {      ...      contact: {        name: "gRPC-Gateway project";        url:
    "https://github.com/grpc-ecosystem/grpc-gateway";        email:
    "none@example.com";      };      ...    };    ...  };
    """

    name: str = betterproto.string_field(1)
    """The identifying name of the contact person/organization."""

    url: str = betterproto.string_field(2)
    """
    The URL pointing to the contact information. MUST be in the format of a
    URL.
    """

    email: str = betterproto.string_field(3)
    """
    The email address of the contact person/organization. MUST be in the format
    of an email address.
    """


@dataclass(eq=False, repr=False)
class License(betterproto.Message):
    """
    `License` is a representation of OpenAPI v2 specification's License object.
    See: https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#licenseObject Example:  option
    (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_swagger) = {    info:
    {      ...      license: {        name: "BSD 3-Clause License";        url:
    "https://github.com/grpc-ecosystem/grpc-gateway/blob/master/LICENSE.txt";
    };      ...    };    ...  };
    """

    name: str = betterproto.string_field(1)
    """The license name used for the API."""

    url: str = betterproto.string_field(2)
    """
    A URL to the license used for the API. MUST be in the format of a URL.
    """


@dataclass(eq=False, repr=False)
class ExternalDocumentation(betterproto.Message):
    """
    `ExternalDocumentation` is a representation of OpenAPI v2 specification's
    ExternalDocumentation object. See: https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#externalDocumentationObject
    Example:  option
    (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_swagger) = {    ...
    external_docs: {      description: "More about gRPC-Gateway";      url:
    "https://github.com/grpc-ecosystem/grpc-gateway";    }    ...  };
    """

    description: str = betterproto.string_field(1)
    """
    A short description of the target documentation. GFM syntax can be used for
    rich text representation.
    """

    url: str = betterproto.string_field(2)
    """
    The URL for the target documentation. Value MUST be in the format of a URL.
    """


@dataclass(eq=False, repr=False)
class Schema(betterproto.Message):
    """
    `Schema` is a representation of OpenAPI v2 specification's Schema object.
    See: https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#schemaObject
    """

    json_schema: "JsonSchema" = betterproto.message_field(1)
    discriminator: str = betterproto.string_field(2)
    """
    Adds support for polymorphism. The discriminator is the schema property
    name that is used to differentiate between other schema that inherit this
    schema. The property name used MUST be defined at this schema and it MUST
    be in the required property list. When used, the value MUST be the name of
    this schema or any schema that inherits it.
    """

    read_only: bool = betterproto.bool_field(3)
    """
    Relevant only for Schema "properties" definitions. Declares the property as
    "read only". This means that it MAY be sent as part of a response but MUST
    NOT be sent as part of the request. Properties marked as readOnly being
    true SHOULD NOT be in the required list of the defined schema. Default
    value is false.
    """

    external_docs: "ExternalDocumentation" = betterproto.message_field(5)
    """Additional external documentation for this schema."""

    example: str = betterproto.string_field(6)
    """
    A free-form property to include an example of an instance for this schema
    in JSON. This is copied verbatim to the output.
    """


@dataclass(eq=False, repr=False)
class JsonSchema(betterproto.Message):
    """
    `JSONSchema` represents properties from JSON Schema taken, and as used, in
    the OpenAPI v2 spec. This includes changes made by OpenAPI v2. See:
    https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#schemaObject See also:
    https://cswr.github.io/JsonSchema/spec/basic_types/,
    https://github.com/json-schema-org/json-schema-spec/blob/master/schema.json
    Example:  message SimpleMessage {    option
    (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_schema) = {
    json_schema: {        title: "SimpleMessage"        description: "A simple
    message."        required: ["id"]      }    };    // Id represents the
    message identifier.    string id = 1; [
    (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_field) = {
    description: "The unique identifier of the simple message."        }];  }
    """

    ref: str = betterproto.string_field(3)
    """
    Ref is used to define an external reference to include in the message. This
    could be a fully qualified proto message reference, and that type must be
    imported into the protofile. If no message is identified, the Ref will be
    used verbatim in the output. For example:  `ref:
    ".google.protobuf.Timestamp"`.
    """

    title: str = betterproto.string_field(5)
    """The title of the schema."""

    description: str = betterproto.string_field(6)
    """A short description of the schema."""

    default: str = betterproto.string_field(7)
    read_only: bool = betterproto.bool_field(8)
    example: str = betterproto.string_field(9)
    """
    A free-form property to include a JSON example of this field. This is
    copied verbatim to the output swagger.json. Quotes must be escaped. This
    property is the same for 2.0 and 3.0.0 https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/3.0.0.md#schemaObject
    https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#schemaObject
    """

    multiple_of: float = betterproto.double_field(10)
    maximum: float = betterproto.double_field(11)
    """
    Maximum represents an inclusive upper limit for a numeric instance. The
    value of MUST be a number,
    """

    exclusive_maximum: bool = betterproto.bool_field(12)
    minimum: float = betterproto.double_field(13)
    """
    minimum represents an inclusive lower limit for a numeric instance. The
    value of MUST be a number,
    """

    exclusive_minimum: bool = betterproto.bool_field(14)
    max_length: int = betterproto.uint64_field(15)
    min_length: int = betterproto.uint64_field(16)
    pattern: str = betterproto.string_field(17)
    max_items: int = betterproto.uint64_field(20)
    min_items: int = betterproto.uint64_field(21)
    unique_items: bool = betterproto.bool_field(22)
    max_properties: int = betterproto.uint64_field(24)
    min_properties: int = betterproto.uint64_field(25)
    required: List[str] = betterproto.string_field(26)
    array: List[str] = betterproto.string_field(34)
    """Items in 'array' must be unique."""

    type: List["JsonSchemaJsonSchemaSimpleTypes"] = betterproto.enum_field(35)
    format: str = betterproto.string_field(36)
    """`Format`"""

    enum: List[str] = betterproto.string_field(46)
    """
    Items in `enum` must be unique https://tools.ietf.org/html/draft-fge-json-
    schema-validation-00#section-5.5.1
    """

    field_configuration: "JsonSchemaFieldConfiguration" = betterproto.message_field(
        1001
    )
    """
    Additional field level properties used when generating the OpenAPI v2 file.
    """

    extensions: Dict[
        str, "betterproto_lib_google_protobuf.Value"
    ] = betterproto.map_field(48, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)


@dataclass(eq=False, repr=False)
class JsonSchemaFieldConfiguration(betterproto.Message):
    """
    'FieldConfiguration' provides additional field level properties used when
    generating the OpenAPI v2 file. These properties are not defined by
    OpenAPIv2, but they are used to control the generation.
    """

    path_param_name: str = betterproto.string_field(47)
    """
    Alternative parameter name when used as path parameter. If set, this will
    be used as the complete parameter name when this field is used as a path
    parameter. Use this to avoid having auto generated path parameter names for
    overlapping paths.
    """


@dataclass(eq=False, repr=False)
class Tag(betterproto.Message):
    """
    `Tag` is a representation of OpenAPI v2 specification's Tag object. See:
    https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#tagObject
    """

    description: str = betterproto.string_field(2)
    """
    A short description for the tag. GFM syntax can be used for rich text
    representation.
    """

    external_docs: "ExternalDocumentation" = betterproto.message_field(3)
    """Additional external documentation for this tag."""


@dataclass(eq=False, repr=False)
class SecurityDefinitions(betterproto.Message):
    """
    `SecurityDefinitions` is a representation of OpenAPI v2 specification's
    Security Definitions object. See: https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#securityDefinitionsObject A
    declaration of the security schemes available to be used in the
    specification. This does not enforce the security schemes on the operations
    and only serves to provide the relevant details for each scheme.
    """

    security: Dict[str, "SecurityScheme"] = betterproto.map_field(
        1, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    """
    A single security scheme definition, mapping a "name" to the scheme it
    defines.
    """


@dataclass(eq=False, repr=False)
class SecurityScheme(betterproto.Message):
    """
    `SecurityScheme` is a representation of OpenAPI v2 specification's Security
    Scheme object. See: https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#securitySchemeObject Allows the
    definition of a security scheme that can be used by the operations.
    Supported schemes are basic authentication, an API key (either as a header
    or as a query parameter) and OAuth2's common flows (implicit, password,
    application and access code).
    """

    type: "SecuritySchemeType" = betterproto.enum_field(1)
    """
    The type of the security scheme. Valid values are "basic", "apiKey" or
    "oauth2".
    """

    description: str = betterproto.string_field(2)
    """A short description for security scheme."""

    name: str = betterproto.string_field(3)
    """
    The name of the header or query parameter to be used. Valid for apiKey.
    """

    in_: "SecuritySchemeIn" = betterproto.enum_field(4)
    """
    The location of the API key. Valid values are "query" or "header". Valid
    for apiKey.
    """

    flow: "SecuritySchemeFlow" = betterproto.enum_field(5)
    """
    The flow used by the OAuth2 security scheme. Valid values are "implicit",
    "password", "application" or "accessCode". Valid for oauth2.
    """

    authorization_url: str = betterproto.string_field(6)
    """
    The authorization URL to be used for this flow. This SHOULD be in the form
    of a URL. Valid for oauth2/implicit and oauth2/accessCode.
    """

    token_url: str = betterproto.string_field(7)
    """
    The token URL to be used for this flow. This SHOULD be in the form of a
    URL. Valid for oauth2/password, oauth2/application and oauth2/accessCode.
    """

    scopes: "Scopes" = betterproto.message_field(8)
    """
    The available scopes for the OAuth2 security scheme. Valid for oauth2.
    """

    extensions: Dict[
        str, "betterproto_lib_google_protobuf.Value"
    ] = betterproto.map_field(9, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)


@dataclass(eq=False, repr=False)
class SecurityRequirement(betterproto.Message):
    """
    `SecurityRequirement` is a representation of OpenAPI v2 specification's
    Security Requirement object. See: https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#securityRequirementObject Lists
    the required security schemes to execute this operation. The object can
    have multiple security schemes declared in it which are all required (that
    is, there is a logical AND between the schemes). The name used for each
    property MUST correspond to a security scheme declared in the Security
    Definitions.
    """

    security_requirement: Dict[
        str, "SecurityRequirementSecurityRequirementValue"
    ] = betterproto.map_field(1, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)
    """
    Each name must correspond to a security scheme which is declared in the
    Security Definitions. If the security scheme is of type "oauth2", then the
    value is a list of scope names required for the execution. For other
    security scheme types, the array MUST be empty.
    """


@dataclass(eq=False, repr=False)
class SecurityRequirementSecurityRequirementValue(betterproto.Message):
    """
    If the security scheme is of type "oauth2", then the value is a list of
    scope names required for the execution. For other security scheme types,
    the array MUST be empty.
    """

    scope: List[str] = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class Scopes(betterproto.Message):
    """
    `Scopes` is a representation of OpenAPI v2 specification's Scopes object.
    See: https://github.com/OAI/OpenAPI-
    Specification/blob/3.0.0/versions/2.0.md#scopesObject Lists the available
    scopes for an OAuth2 security scheme.
    """

    scope: Dict[str, str] = betterproto.map_field(
        1, betterproto.TYPE_STRING, betterproto.TYPE_STRING
    )
    """
    Maps between a name of a scope to a short description of it (as the value
    of the property).
    """
