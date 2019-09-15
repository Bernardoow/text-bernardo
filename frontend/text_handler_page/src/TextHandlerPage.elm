module TextHandlerPage exposing (Model, Msg(..), init, main, update, view)

import Browser
import Dict
import Html exposing (Html, a, button, div, h1, img, input, label, li, p, strong, text, textarea, ul)
import Html.Attributes exposing (attribute, class, for, href, id, type_, value)
import Html.Events exposing (onClick, onInput)
import Http
import Json.Decode as Decode
import Json.Encode as Encode



---- MODEL ----


type alias Model =
    { vision : Vision }


init : ( Model, Cmd Msg )
init =
    ( { vision = SendText { input = "", message = Nothing } }, Cmd.none )



---- UPDATE ----


type MessageType
    = MTSucess
    | MTDanger


type alias Message =
    { text : String, type_ : MessageType }


type alias SendTextModel =
    { input : String
    , message : Maybe Message
    }


type alias IsolatedVocabularyModel =
    { vocabulary : Maybe (List String)
    }


type alias IsolatedFrequencyModel =
    { vocabulary : Maybe (List String)
    , frequency : Maybe (Dict.Dict String (List Int))
    }


type alias GranNFrequencyModel =
    { vocabulary : Maybe (List (List String))
    , frequency : Maybe (Dict.Dict String (List Int))
    }


type alias GranNVocabularyModel =
    { vocabulary : Maybe (List (List String))
    }


type Vision
    = SendText SendTextModel
    | IsolatedVocabulary IsolatedVocabularyModel
    | GranNVocabulary GranNVocabularyModel
    | IsolatedFrequency IsolatedFrequencyModel
    | GranNFrequency GranNFrequencyModel


type Msg
    = OnInputText String
    | OnClickSendText
    | OnClickChangeVision Vision
    | OnResponseCreateText (Result Http.Error ())
    | OnResponseIsolatedVocabulary (Result Http.Error (List String))
    | OnResponseGranNVocabulary (Result Http.Error (List (List String)))
    | OnResponseFrequency (Result Http.Error (Dict.Dict String (List Int)))


createText : Encode.Value -> Cmd Msg
createText value =
    Http.post
        { url = "http://127.0.0.1:5000/api/v1/send-text"
        , body = Http.jsonBody value
        , expect = Http.expectWhatever OnResponseCreateText
        }


getIsolatedVocabulary : Cmd Msg
getIsolatedVocabulary =
    Http.get
        { url = "http://127.0.0.1:5000/api/v1/isolated-vocabulary"
        , expect = Http.expectJson OnResponseIsolatedVocabulary (Decode.field "vocabulary" (Decode.list Decode.string))
        }


getGranNVocabulary : Cmd Msg
getGranNVocabulary =
    Http.get
        { url = "http://127.0.0.1:5000/api/v1/ngran-vocabulary"
        , expect = Http.expectJson OnResponseGranNVocabulary (Decode.field "vocabulary" (Decode.list (Decode.list Decode.string)))
        }


getIsolatedFrequency : Cmd Msg
getIsolatedFrequency =
    Http.get
        { url = "http://127.0.0.1:5000/api/v1/isolated-frequency-distribution"
        , expect = Http.expectJson OnResponseFrequency (Decode.field "frequency" (Decode.dict (Decode.list Decode.int)))
        }


getGramNFrequency : Cmd Msg
getGramNFrequency =
    Http.get
        { url = "http://127.0.0.1:5000/api/v1/ngran-frequency-distribution"
        , expect = Http.expectJson OnResponseFrequency (Decode.field "frequency" (Decode.dict (Decode.list Decode.int)))
        }


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        OnInputText text ->
            case model.vision of
                SendText sendTextModel ->
                    ( { model | vision = SendText { sendTextModel | input = text } }, Cmd.none )

                _ ->
                    ( model, Cmd.none )

        OnClickSendText ->
            case model.vision of
                SendText sendTextModel ->
                    let
                        value =
                            Encode.object [ ( "text", Encode.string sendTextModel.input ) ]
                    in
                    ( model, createText value )

                _ ->
                    ( model, Cmd.none )

        OnResponseCreateText (Ok ()) ->
            case model.vision of
                SendText sendTextModel ->
                    ( { model | vision = SendText { sendTextModel | input = "", message = Just { text = "Texto cadastrado com sucesso!", type_ = MTSucess } } }, Cmd.none )

                _ ->
                    ( model, Cmd.none )

        OnResponseCreateText (Err error) ->
            case model.vision of
                SendText sendTextModel ->
                    ( { model | vision = SendText { sendTextModel | input = "", message = Just { text = "Aconteceu algum problema na requisição.", type_ = MTDanger } } }, Cmd.none )

                _ ->
                    ( model, Cmd.none )

        OnClickChangeVision vision ->
            case vision of
                SendText _ ->
                    ( { model | vision = vision }, Cmd.none )

                IsolatedVocabulary _ ->
                    ( { model | vision = vision }, getIsolatedVocabulary )

                GranNVocabulary _ ->
                    ( { model | vision = vision }, getGranNVocabulary )

                IsolatedFrequency _ ->
                    ( { model | vision = vision }, Cmd.batch [ getIsolatedVocabulary, getIsolatedFrequency ] )

                GranNFrequency _ ->
                    ( { model | vision = vision }, Cmd.batch [ getGranNVocabulary, getGramNFrequency ] )

        OnResponseIsolatedVocabulary (Ok vocabulary) ->
            case model.vision of
                IsolatedVocabulary _ ->
                    ( { model | vision = IsolatedVocabulary { vocabulary = Just vocabulary } }, Cmd.none )

                IsolatedFrequency isolatedFrequencyModel ->
                    ( { model | vision = IsolatedFrequency { isolatedFrequencyModel | vocabulary = Just vocabulary } }, Cmd.none )

                _ ->
                    ( model, Cmd.none )

        OnResponseIsolatedVocabulary (Err _) ->
            ( model, Cmd.none )

        OnResponseGranNVocabulary (Ok vocabulary) ->
            case model.vision of
                GranNVocabulary _ ->
                    ( { model | vision = GranNVocabulary { vocabulary = Just vocabulary } }, Cmd.none )

                GranNFrequency granNVocabularyModel ->
                    ( { model | vision = GranNFrequency { granNVocabularyModel | vocabulary = Just vocabulary } }, Cmd.none )

                _ ->
                    ( model, Cmd.none )

        OnResponseGranNVocabulary (Err _) ->
            ( model, Cmd.none )

        OnResponseFrequency (Ok frequency) ->
            case model.vision of
                IsolatedFrequency isolatedFrequencyModel ->
                    ( { model | vision = IsolatedFrequency { isolatedFrequencyModel | frequency = Just frequency } }, Cmd.none )

                GranNFrequency granNVocabularyModel ->
                    ( { model | vision = GranNFrequency { granNVocabularyModel | frequency = Just frequency } }, Cmd.none )

                _ ->
                    ( model, Cmd.none )

        OnResponseFrequency (Err _) ->
            ( model, Cmd.none )



---- VIEW ----


handleActite : Int -> Vision -> String
handleActite pos vision =
    case vision of
        SendText _ ->
            if 1 == pos then
                "active"

            else
                ""

        IsolatedVocabulary _ ->
            if 2 == pos then
                "active"

            else
                ""

        GranNVocabulary _ ->
            if 3 == pos then
                "active"

            else
                ""

        IsolatedFrequency _ ->
            if 4 == pos then
                "active"

            else
                ""

        GranNFrequency _ ->
            if 5 == pos then
                "active"

            else
                ""


view : Model -> Html Msg
view model =
    div [ class "container" ]
        [ ul [ class "nav nav-pills nav-fill" ]
            [ li [ onClick <| OnClickChangeVision (SendText { input = "", message = Nothing }), class "nav-item" ]
                [ a [ id "newText", class "nav-link", class <| handleActite 1 model.vision, href "#" ]
                    [ text "Criar texto" ]
                ]
            , li [ onClick <| OnClickChangeVision <| IsolatedVocabulary { vocabulary = Nothing }, class "nav-item" ]
                [ a [ id "vocabularySimples", class <| handleActite 2 model.vision, class "nav-link", href "#" ]
                    [ text "Mostrar Vocabulário Simples" ]
                ]
            , li [ onClick <| OnClickChangeVision <| GranNVocabulary { vocabulary = Nothing }, class "nav-item" ]
                [ a [ id "vocabulary2Gram", class <| handleActite 3 model.vision, class "nav-link", href "#" ]
                    [ text "Mostrar Vocabulário 2Palavras" ]
                ]
            , li [ onClick <| OnClickChangeVision <| IsolatedFrequency { vocabulary = Nothing, frequency = Nothing }, class "nav-item" ]
                [ a [ id "frequencySimples", class <| handleActite 4 model.vision, class "nav-link", href "#" ]
                    [ text "Mostrar Frequência Simples" ]
                ]
            , li [ onClick <| OnClickChangeVision <| GranNFrequency { vocabulary = Nothing, frequency = Nothing }, class "nav-item" ]
                [ a [ id "frequency2Gram", class <| handleActite 5 model.vision, class "nav-link", href "#" ]
                    [ text "Mostrar Frequência 2Palavras" ]
                ]
            ]
        , case model.vision of
            SendText sendTextModel ->
                div [ class "row" ]
                    [ case sendTextModel.message of
                        Nothing ->
                            text ""

                        Just message ->
                            case message.type_ of
                                MTSucess ->
                                    div [ class "col-12" ]
                                        [ p [ class "alert alert-success" ] [ text message.text ]
                                        ]

                                MTDanger ->
                                    div [ class "col-12" ]
                                        [ p [ class "alert alert-danger" ] [ text message.text ]
                                        ]
                    , div [ class "col-12" ]
                        [ div [ class "form-group" ]
                            [ label [ for "textTextArea" ]
                                [ text "Digite seu texto" ]
                            , textarea [ onInput OnInputText, class "form-control", id "textTextArea", value sendTextModel.input ]
                                []
                            ]
                        ]
                    , button [ onClick OnClickSendText, class "btn btn-primary" ] [ text "Cadastrar texto" ]
                    ]

            IsolatedVocabulary isolatedVocabularyModel ->
                case isolatedVocabularyModel.vocabulary of
                    Nothing ->
                        p [ class "alert alert-info" ] [ text "Carregando...." ]

                    Just vocabulary ->
                        let
                            vocabularyList =
                                List.map (\word -> li [ class "list-group-item" ] [ text word ]) vocabulary
                                    |> ul [ class "list-group" ]
                        in
                        div [ class "row" ]
                            [ div [ class "col-12" ] [ strong [] [ text "Vocabulário" ] ]
                            , div [ class "col-12" ]
                                [ vocabularyList ]
                            ]

            GranNVocabulary granNVocabularyModel ->
                case granNVocabularyModel.vocabulary of
                    Nothing ->
                        p [ class "alert alert-info" ] [ text "Carregando...." ]

                    Just vocabulary ->
                        let
                            vocabularyList =
                                List.map (\listWord -> li [ class "list-group-item" ] [ text <| String.join " " listWord ]) vocabulary
                                    |> ul [ class "list-group" ]
                        in
                        div [ class "row" ]
                            [ div [ class "col-12" ] [ strong [] [ text "Vocabulário" ] ]
                            , div [ class "col-12" ]
                                [ vocabularyList ]
                            ]

            IsolatedFrequency isolatedFrequencyModel ->
                case ( isolatedFrequencyModel.vocabulary, isolatedFrequencyModel.frequency ) of
                    ( Just vocabulary, Just frequency ) ->
                        let
                            vocabularyList =
                                List.map (\word -> li [ class "list-group-item" ] [ text word ]) vocabulary
                                    |> ul [ class "list-group" ]

                            frequencyList =
                                Dict.values frequency
                                    |> List.map
                                        (\frequencyListValue ->
                                            li [ class "list-group-item" ]
                                                [ List.map String.fromInt frequencyListValue
                                                    |> String.join ", "
                                                    |> text
                                                ]
                                        )
                                    |> ul [ class "list-group" ]
                        in
                        div [ class "row" ]
                            [ div [ class "col-12" ] [ strong [] [ text "Vocabulário" ] ]
                            , div [ class "col-6" ]
                                [ vocabularyList ]
                            , div [ class "col-6" ]
                                [ frequencyList ]
                            ]

                    ( _, _ ) ->
                        p [ class "alert alert-info" ] [ text "Carregando...." ]

            GranNFrequency granNFrequencyModel ->
                case ( granNFrequencyModel.vocabulary, granNFrequencyModel.frequency ) of
                    ( Just vocabulary, Just frequency ) ->
                        let
                            vocabularyList =
                                List.map (\listWord -> li [ class "list-group-item" ] [ text <| String.join " " listWord ]) vocabulary
                                    |> ul [ class "list-group" ]

                            frequencyList =
                                Dict.values frequency
                                    |> List.map
                                        (\frequencyListValue ->
                                            li [ class "list-group-item" ]
                                                [ List.map String.fromInt frequencyListValue
                                                    |> String.join ", "
                                                    |> text
                                                ]
                                        )
                                    |> ul [ class "list-group" ]
                        in
                        div [ class "row" ]
                            [ div [ class "col-12" ] [ strong [] [ text "Vocabulário" ] ]
                            , div [ class "col-6" ]
                                [ vocabularyList ]
                            , div [ class "col-6" ]
                                [ frequencyList ]
                            ]

                    ( _, _ ) ->
                        p [ class "alert alert-info" ] [ text "Carregando...." ]
        ]



---- PROGRAM ----


main : Program () Model Msg
main =
    Browser.element
        { view = view
        , init = \_ -> init
        , update = update
        , subscriptions = always Sub.none
        }
