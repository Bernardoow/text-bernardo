module TextHandlerPageTest exposing (start, suite)

import Expect exposing (Expectation)
import Fuzz exposing (Fuzzer, int, list, string)
import ProgramTest as PT
import Test exposing (..)
import Test.Html.Query as Query
import Test.Html.Selector as Selector
import TextHandlerPage as Main


start : PT.ProgramTest Main.Model Main.Msg (Cmd Main.Msg)
start =
    PT.createElement
        { init = \_ -> Main.init
        , update = Main.update
        , view = Main.view
        }
        |> PT.start ()


suite : Test
suite =
    describe "smoke test"
        [ test "should has a bootstrap nav" <|
            \() ->
                start
                    |> PT.expectViewHas
                        [ Selector.tag "ul"
                        , Selector.classes [ "nav", "nav-pills", "nav-fill" ]
                        , Selector.containing
                            [ Selector.all
                                [ Selector.tag "li"
                                , Selector.class "nav-item"
                                ]
                            ]
                        ]

        -- , test "should has a nav with items" <|
        --     \() ->
        --         start
        --             |> PT.expectViewHas
        --                 [ Selector.tag "li"
        --                 , Selector.classes [ "nav-item" ]
        --                 , Selector.containing
        --                     [ Selector.all
        --                         [ Selector.tag "a"
        --                         , Selector.class "nav-link"
        --                         , Selector.containing [ Selector.text "Criar texto" ]
        --                         ]
        --                     ]
        --                 , Selector.containing
        --                     [ Selector.all
        --                         [ Selector.tag "a"
        --                         , Selector.class "nav-link"
        --                         , Selector.containing [ Selector.text "Mostrar Vocabulário Simples" ]
        --                         ]
        --                     ]
        --                 , Selector.containing
        --                     [ Selector.all
        --                         [ Selector.tag "a"
        --                         , Selector.class "nav-link"
        --                         , Selector.containing [ Selector.text "Mostrar Vocabulário 2Palavras" ]
        --                         ]
        --                     ]
        --                 , Selector.containing
        --                     [ Selector.all
        --                         [ Selector.tag "a"
        --                         , Selector.class "nav-link"
        --                         , Selector.containing [ Selector.text "Mostrar Frequência Simples" ]
        --                         ]
        --                     ]
        --                 , Selector.containing
        --                     [ Selector.all
        --                         [ Selector.tag "a"
        --                         , Selector.class "nav-link"
        --                         , Selector.containing [ Selector.text "Mostrar Frequência 2Palavras" ]
        --                         ]
        --                     ]
        --                 ]
        -- , test "should change active when click in nav link" <|
        --     \() ->
        --         start
        --             |> PT.clickLink "Criar text" ""
        --             |> PT.expectViewHas
        --                 [-- Selector.tag "a"
        --                  -- , Selector.class "active"
        --                  -- , Selector.containing [ Selector.text "Criar texto" ]
        --                 ]
        ]
