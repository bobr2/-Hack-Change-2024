    package com.suir.suir;

    import com.fasterxml.jackson.databind.ObjectMapper;
    import org.apache.commons.io.IOUtils;
    import org.springframework.http.HttpStatus;
    import org.springframework.http.ResponseEntity;
    import org.springframework.web.bind.annotation.ExceptionHandler;
    import org.springframework.web.bind.annotation.PostMapping;
    import org.springframework.web.bind.annotation.RequestBody;
    import org.springframework.web.bind.annotation.RestController;

    import java.io.IOException;
    import java.io.InputStream;
    import java.nio.charset.StandardCharsets;
    import java.util.HashMap;
    import java.util.Map;

    @RestController
    public class Backend {

        @PostMapping("/process")
        public String post() throws IOException {
            try {

                //путь к json файлу с инфой о пользователе
                String filePath = ".//src//main//java//com//suir//suir//example.json"; //<---------- В СЛУЧАЕ ОШИБКИ, ВСТАВЬТЕ АКТУАЛЬНОЕ НАЗВАНИЕ ВХОДНОГО ФАЙЛЯ СЮДА

                ProcessBuilder pb = new ProcessBuilder("python",
                        ".//src//main//java//com//suir//py//otlad1.py", //скрипт
                        filePath); //json файл

                pb.redirectErrorStream(true); //объединяем поток вывода и ошибок, чтобы можно было обрабатывать их вместе

                Process process = pb.start(); //запуск процесса выполнения скрипта


                InputStream is = process.getInputStream();
                String resultString = IOUtils.toString(is, StandardCharsets.UTF_8);

                //Десериализация JSON строки в Map
                ObjectMapper objectMapper = new ObjectMapper();
                Map<String, Object> jsonMap = objectMapper.readValue(resultString, Map.class);

                // Форматирование и вывод отформатированного JSON
                String formattedJson = objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(jsonMap);
                System.out.println(formattedJson);
                return formattedJson;

            } catch (IOException e) {

                throw e;

            } catch (Exception e) {
                //e.printStackTrace(); // Обработка других исключений
                throw e;
            }
        }

        /*@ExceptionHandler(Exception.class)
        public ResponseEntity<Map<String, Object>> handleException(Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("status", "error");
            response.put("message", e.getMessage()); // Сообщение об ошибке

            // Ключевой момент: детали стека вызовов
            StackTraceElement[] stackTrace = e.getStackTrace();
            StringBuilder stackTraceString = new StringBuilder();
            for (StackTraceElement element : stackTrace) {
                stackTraceString.append(element.toString()).append("\n");
            }
            response.put("stackTrace", stackTraceString.toString());


            // Важно: Укажите, где произошла ошибка. Используйте toString() для более понятных строк.
            response.put("errorCode", e.getClass().getSimpleName() );
            response.put("errorLocation", e.getStackTrace()[0].toString());


            return new ResponseEntity<>(response, HttpStatus.INTERNAL_SERVER_ERROR);
        }*/
    }
