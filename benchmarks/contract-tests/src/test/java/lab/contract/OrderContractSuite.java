package lab.contract;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Identical, inherited HTTP acceptance tests for every runnable backend profile.
 * Do not edit this oracle inside individual agent benchmark trials.
 */
public abstract class OrderContractSuite {
    @Autowired protected MockMvc mvc;
    private final ObjectMapper mapper = new ObjectMapper();

    protected long create(String name, int quantity) throws Exception {
        String payload = mapper.writeValueAsString(new CreateRequest(name, quantity));
        String body = mvc.perform(post("/api/orders").contentType(MediaType.APPLICATION_JSON).content(payload))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id", greaterThan(0)))
                .andExpect(jsonPath("$.productName").value(name.trim()))
                .andExpect(jsonPath("$.quantity").value(quantity))
                .andExpect(jsonPath("$.status").value("CREATED"))
                .andReturn().getResponse().getContentAsString();
        return mapper.readTree(body).get("id").asLong();
    }

    protected record CreateRequest(String productName, int quantity) {}

    @Test void createAndListAndCancelIdempotently() throws Exception {
        long id = create(" Notebook ", 3);
        mvc.perform(get("/api/orders"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[*].id", hasItem((int) id)))
                .andExpect(jsonPath("$[*].productName", hasItem("Notebook")));
        mvc.perform(post("/api/orders/" + id + "/cancel"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(id))
                .andExpect(jsonPath("$.status").value("CANCELLED"));
        mvc.perform(post("/api/orders/" + id + "/cancel"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("CANCELLED"));
    }

    @Test void invalidInputProduces400() throws Exception {
        mvc.perform(post("/api/orders").contentType(MediaType.APPLICATION_JSON)
                .content("{\"productName\":\"  \",\"quantity\":1}"))
                .andExpect(status().isBadRequest());
        mvc.perform(post("/api/orders").contentType(MediaType.APPLICATION_JSON)
                .content("{\"productName\":\"Pencil\",\"quantity\":0}"))
                .andExpect(status().isBadRequest());
        mvc.perform(post("/api/orders").contentType(MediaType.APPLICATION_JSON)
                .content("{\"productName\":\"Pencil\"}"))
                .andExpect(status().isBadRequest());
    }

    @Test void missingOrderProduces404() throws Exception {
        mvc.perform(post("/api/orders/999999999/cancel")).andExpect(status().isNotFound());
    }
}
