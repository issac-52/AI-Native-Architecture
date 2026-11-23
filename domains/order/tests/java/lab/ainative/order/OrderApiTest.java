package lab.ainative.order;

import lab.ainative.ApiApplication;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.hamcrest.Matchers.*;

@SpringBootTest(classes = ApiApplication.class)
@AutoConfigureMockMvc
class OrderApiTest {
    @Autowired MockMvc mvc;

    @Test void createListCancelTwice() throws Exception {
        String body = "{\"productName\":\"Book\",\"quantity\":2}";
        String json = mvc.perform(post("/api/orders").contentType(MediaType.APPLICATION_JSON).content(body))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.status").value("CREATED"))
            .andReturn().getResponse().getContentAsString();
        long id = Long.parseLong(json.replaceAll(".*\\\"id\\\":([0-9]+).*", "$1"));
        mvc.perform(get("/api/orders")).andExpect(status().isOk())
            .andExpect(jsonPath("$[*].productName", hasItem("Book")));
        mvc.perform(post("/api/orders/" + id + "/cancel")).andExpect(status().isOk())
            .andExpect(jsonPath("$.status").value("CANCELLED"));
        mvc.perform(post("/api/orders/" + id + "/cancel")).andExpect(status().isOk())
            .andExpect(jsonPath("$.status").value("CANCELLED"));
    }

    @Test void invalidAndUnknown() throws Exception {
        mvc.perform(post("/api/orders").contentType(MediaType.APPLICATION_JSON)
            .content("{\"productName\":\"  \",\"quantity\":1}")).andExpect(status().isBadRequest());
        mvc.perform(post("/api/orders").contentType(MediaType.APPLICATION_JSON)
            .content("{\"productName\":\"A\",\"quantity\":0}")).andExpect(status().isBadRequest());
        mvc.perform(post("/api/orders/999999/cancel")).andExpect(status().isNotFound());
    }
}
