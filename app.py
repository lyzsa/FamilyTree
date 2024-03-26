import math
import gradio as gr
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np


class person_p:
    def __init__(self, attributes, relationship) -> None:
        self.attributes = attributes
        self.seniors = []
        self.peers = []
        self.juniors = []
        self.age_level = 0

    def update(self, update_data):
        for key, value in update_data.items():
            if key in self.attributes and value != "":
                self.attributes[key] = value


class family:
    def __init__(self) -> None:
        self.people = []
        self.ids = []

    def add(self, person, id_):
        self.people.append(person)
        self.ids.append(id_)

    def update(self, update_values, id_):
        for index, id_t in enumerate(self.ids):
            if id_t == id_:
                self.people[index].update(update_values)
                return


fam = family()


def clear_all(
    identity,
    fn,
    ln,
    lnb,
    living,
    gen,
    birth_mon,
    birth_day,
    birth_year,
    relationship,
    relathipship_id,
    contect,
    bio,
):
    return ["", "", "", "", False, None, None, None, "", "", "", None, ""]


def add_person(
    identity,
    fn,
    ln,
    lnb,
    living,
    gen,
    birth_mon,
    birth_day,
    birth_year,
    relationship,
    relationship_id,
    contact,
    bio,
):
    update_values = {}
    update_values["identity"] = identity
    update_values["first_name"] = fn
    update_values["last_name"] = ln
    update_values["gender"] = gen
    update_values["last_name_birth"] = lnb
    update_values["living"] = living
    update_values["birth_month"] = birth_mon
    update_values["birth_day"] = birth_day
    update_values["birth_year"] = birth_year
    update_values["relationship"] = relationship
    update_values["relationship_id"] = relationship_id
    update_values["contact"] = contact
    update_values["bio"] = bio
    if identity in fam.ids:
        fam.update(update_values, identity)
    else:
        fam.add(person_p(update_values, relationship_id), identity)
    current_index = fam.ids.index(identity)
    if identity != "Me":
        if relationship_id not in fam.ids:
            return "Please input an identity recorded!!!", go.Figure()
        index = fam.ids.index(relationship_id)
        if relationship == "Senior":
            fam.people[index].seniors.append(identity)
            fam.people[current_index].age_level = fam.people[index].age_level - 1
        elif relationship == "Peer":
            fam.people[index].peers.append(identity)
            fam.people[current_index].age_level = fam.people[index].age_level
        else:
            fam.people[index].juniors.append(identity)
            fam.people[current_index].age_level = fam.people[index].age_level + 1
    else:
        fam.people[current_index].age_level = 0
    ages_levels = [per.age_level for per in fam.people]
    sort_index = np.argsort(np.array(ages_levels))
    fam.people = [fam.people[i] for i in sort_index]
    fam.ids = [fam.ids[i] for i in sort_index]
    pos = {}
    current_x = 0
    current_y = 0
    xn = []
    yn = []
    annotations = []
    color_ops = []
    org_color = 55
    current_level = fam.people[0].age_level - 1
    for index, person in enumerate(fam.people):
        if person.age_level != current_level:
            current_x = 0
            current_y -= 0.25
            current_level = person.age_level
        else:
            current_x += 0.25
        color_ops.append("rgb(" + str(50 + person.age_level * 5) + ",50,50)")
        pos[person.attributes["identity"]] = (current_x, current_y)
        xn.append(current_x)
        yn.append(current_y)
        annotations.append(
            dict(
                text=person.attributes["identity"],
                # + ":\n"
                # + person.attributes["first_name"]
                # + "\n"
                # + person.attributes[
                #     "last_name"
                # ],  # or replace labels with a different list for the text within the circle
                x=current_x,
                y=current_y,
                xref="x1",
                yref="y1",
                font=dict(color="rgb(250,250,250)", size=15),
                showarrow=False,
            )
        )
    xe = []
    ye = []
    for index, person in enumerate(fam.people):
        current_id = person.attributes["identity"]
        for senior in person.seniors:
            xe.append([pos[current_id][0], pos[senior][0]])
            ye.append([pos[current_id][1], pos[senior][1]])
        for peer in person.peers:
            xe.append([pos[current_id][0], pos[peer][0]])
            ye.append([pos[current_id][1], pos[peer][1]])
        for junior in person.juniors:
            xe.append([pos[current_id][0], pos[junior][0]])
            ye.append([pos[current_id][1], pos[junior][1]])
    fig = go.Figure()

    for zip_x, zip_y in zip(xe, ye):
        fig.add_trace(
            go.Scatter(
                x=zip_x,
                y=zip_y,
                mode="lines",
                line=dict(color="rgb(210,210,210)", width=1),
                hoverinfo="none",
            )
        )
    for index, xn_ in enumerate(xn):
        fig.add_trace(
            go.Scatter(
                x=[xn_],
                y=[yn[index]],
                mode="markers",
                name="bla",
                marker=dict(
                    symbol="circle-dot",
                    size=50,
                    color=color_ops[index],  #'#DB4551',
                    line=dict(color="rgb(50,50,50)", width=1),
                ),
                hoverinfo="text",
                opacity=0.8,
            )
        )
    axis = dict(
        showline=False,  # hide axis line, grid, ticklabels and  title
        zeroline=False,
        showgrid=False,
        showticklabels=False,
    )

    fig.update_layout(
        title="",
        annotations=annotations,
        font_size=12,
        showlegend=False,
        xaxis=axis,
        yaxis=axis,
        margin=dict(l=40, r=40, b=85, t=100),
        hovermode="closest",
        plot_bgcolor="rgb(248,248,248)",
    )
    fig.update_layout(
        width=1000,
        height=1000,
    )
    return identity, fig


def present_info(identity):
    if identity in fam.ids:
        values = fam.people[fam.ids.index(identity)]
        return list(values.attributes.values())
    return [
        "This person's information is not recorded!!!",
        "",
        "",
        "",
        False,
        None,
        None,
        None,
        "",
        "",
        "",
        None,
        "",
    ]


block = gr.Blocks().queue()
with block:
    with gr.Row():
        gr.Markdown("## A dynamic family tree.")
    with gr.Column():
        gr.Label("Family tree:")
        tree = gr.Plot()
    with gr.Row():
        with gr.Tab("Personal"):
            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        identity = gr.Textbox("Identity: (e.g. Me, Father, Mother))")
                        show_info = gr.Button("Show info")
                    fn = gr.Textbox(label="Given names:")
                    ln = gr.Textbox(label="Surname now:")
                    lnb = gr.Textbox(label="Surname at birth:")
                    gen = gr.Radio(["Female", "Male", "Other"], label="Gender:")
                    with gr.Row():
                        gr.Label("Birth date:")
                        birth_mon = gr.Dropdown(
                            [
                                "Jan",
                                "Feb",
                                "Mar",
                                "Apr",
                                "May",
                                "Jun",
                                "Jul",
                                "Aug",
                                "Sept",
                                "Oct",
                                "Nov",
                                "Dec",
                            ],
                            label="",
                        )
                        birth_day = gr.Dropdown(
                            [str(i) for i in range(1, 32)], label=""
                        )
                        birth_year = gr.Textbox(label="")
                    living = gr.Checkbox(label="This person is living", value=False)
                    with gr.Row():
                        relationship = gr.Radio(
                            ["Senior", "Peer", "Junior"], label="Relationship to"
                        )
                        relationship_id = gr.Textbox(label="")
                    with gr.Row():
                        gr.Label("You can also add or change details later")
                        ok_button = gr.Button(value="OK")
                        cancel_button = gr.Button(value="Cancel")
        with gr.Tab("Contact"):
            contact = gr.Textbox("Contact information is: ")
        with gr.Tab("Biography"):
            bio = gr.Textbox("My biography is: ")
    cancel_button.click(
        clear_all,
        inputs=[
            identity,
            fn,
            ln,
            lnb,
            living,
            gen,
            birth_mon,
            birth_day,
            birth_year,
            relationship,
            relationship_id,
            contact,
            bio,
        ],
        outputs=[
            identity,
            fn,
            ln,
            lnb,
            living,
            gen,
            birth_mon,
            birth_day,
            birth_year,
            relationship,
            relationship_id,
            contact,
            bio,
        ],
    )
    ok_button.click(
        add_person,
        inputs=[
            identity,
            fn,
            ln,
            lnb,
            living,
            gen,
            birth_mon,
            birth_day,
            birth_year,
            relationship,
            relationship_id,
            contact,
            bio,
        ],
        outputs=[identity, tree],
    )
    show_info.click(
        present_info,
        inputs=[identity],
        outputs=[
            identity,
            fn,
            ln,
            lnb,
            living,
            gen,
            birth_mon,
            birth_day,
            birth_year,
            relationship,
            relationship_id,
            contact,
            bio,
        ],
    )
block.launch(server_name="0.0.0.0")
